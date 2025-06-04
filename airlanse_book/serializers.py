from rest_framework import serializers
from .models import FlightModel, TicketsModel, UserModel


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'username','first_name','last_name',
            'email','city'
        ]


class FlightModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightModel
        fields = '__all__'


class TicketsModelSerializer(serializers.ModelSerializer):
    flight_detail = FlightModelSerializer(source='flight', read_only=True)
    flight = serializers.PrimaryKeyRelatedField(queryset=FlightModel.objects.all())
    owner = UserModelSerializer(read_only=True)
    ticket_number = serializers.CharField(read_only=True)
    class Meta:
        model = TicketsModel
        fields = '__all__'