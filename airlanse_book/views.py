from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .services.buy_ticket import purchase_ticket
from .serializers import TicketsModelSerializer,UserModelSerializer,FlightModelSerializer
from .models import TicketsModel,FlightModel,UserModel
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, extend_schema_view
import logging

# Create your views here.
logger = logging.getLogger(__name__)

class OwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        has_permission = obj.owner == request.user
        if not has_permission:
            logger.warning(
                f'Access denied: user {request.user} (id={request.user.id}) tried to'
                f'{request.method} object {obj} in view {view.__class__.__name__}'
            )
        return has_permission

class SuperOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user and request.user.is_staff

@extend_schema_view(
    list=extend_schema(summary='Список всех пользователей'),
    retrieve=extend_schema(summary='Получить пользователя по ID'),
    create=extend_schema(summary='Создать пользователя'),
    update=extend_schema(summary='Полное обновление данных'),
    partial_update=extend_schema(summary='Частичное обновление данных'),
    destroy=extend_schema(summary='Удалить пользователя'),
)
class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    list=extend_schema(summary='Список всех билетов'),
    retrieve=extend_schema(summary='Получить билет по FK'),
    create=extend_schema(summary='Создать билет'),
    update=extend_schema(summary='Полное обновление данных'),
    partial_update=extend_schema(summary='Частичное обновление данных'),
    destroy=extend_schema(summary='Удалить билет'),
)
class TicketsViewSet(ModelViewSet):
    queryset = TicketsModel.objects.select_related('flight', 'owner')
    serializer_class = TicketsModelSerializer
    permission_classes = [OwnerOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'patch']

@extend_schema_view(
    list=extend_schema(summary='Список всех рейсов'),
    retrieve=extend_schema(summary='Получить рейс по ID'),
    create=extend_schema(summary='Создать рейс'),
    update=extend_schema(summary='Полное обновление данных'),
    partial_update=extend_schema(summary='Частичное обновление данных'),
    destroy=extend_schema(summary='Удалить рейс'),
)
class FlightsViewSet(ModelViewSet):
    queryset = FlightModel.objects.prefetch_related('tickets')
    serializer_class = FlightModelSerializer
    permission_classes = [SuperOrReadOnly]

    @extend_schema(
        request=None,
        responses=TicketsModelSerializer,
        summary='Покупка билета и его генерация',
        description='Нужен id рейса'
    )
    @action(detail=True, methods=['post'], url_path='purchase')
    def purchase(self, request, pk=None):
        flight = self.get_object()
        user = request.user
        try:
            ticket = purchase_ticket(flight, user)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(TicketsModelSerializer(ticket).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_archived = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    summary='Самый дешевый билет',
    parameters=[
        OpenApiParameter(
            name='city_from',
            type=str,
            description='Город отправления',
            required=True
        ),
        OpenApiParameter(
            name='city_to',
            type=str,
            description='Город прибытия',
            required=True
        ),
    ],
    responses=FlightModelSerializer,
    description='Эндпоинт получения билетов по конкретным городам, по цене'
)
class LowestPriceFlightApiView(APIView):
    def get(self, request):
        city_from = request.query_params.get("city_from")
        city_to = request.query_params.get("city_to")
        flights = FlightModel.objects.filter(city_from=city_from,city_to=city_to).order_by("ticket_price")
        serializer = FlightModelSerializer(flights, many=True)
        return Response(serializer.data)

