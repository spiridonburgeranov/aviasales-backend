from django.contrib import admin
from django.urls import path, include
from airlanse_book.views import FlightsViewSet,UserViewSet,TicketsViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
TokenObtainPairView,
TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


router = DefaultRouter()
router.register(r'flights', FlightsViewSet, basename='flights')
router.register(r'users', UserViewSet, basename='users')
router.register(r'tickets', TicketsViewSet, basename='tickets')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'))
]
