import random
import string
from sys import prefix
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError



# Create your models here.
class FlightStatusModel(models.TextChoices):
    SCHEDULED = 'Scheduled'
    ONTIME = 'On time'
    DELAYED = 'Delayed'
    DEPARTED = 'Departed'
    LANDED = 'Landed'
    CHECK_IN_CLOSED = 'Check in closed'

class FlightModel(models.Model):
    flight_number = models.CharField(max_length=16,blank=False,null=False)
    city_from = models.CharField(max_length=32,blank=False,null=False)
    city_to = models.CharField(max_length=32,blank=False,null=False)
    departure = models.DateTimeField(null=False,blank=False)
    arrival = models.DateTimeField(null=False,blank=False)
    flight_status = models.CharField(default=FlightStatusModel.SCHEDULED, choices=FlightStatusModel)
    tickets_available = models.PositiveIntegerField(blank=False, null=False)
    tickets_status = models.BooleanField(default=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    company = models.CharField(default=None, null=True, blank=True)
    is_archived = models.BooleanField(default=False)


    class Meta:
        db_table = 'flight_table'

    def __str__(self):
        return self.flight_number

    def clean(self):
        if self.tickets_available < 0:
            raise ValidationError('Колличесвто билетов не может быть отрицательным')


    def save(self, *args, **kwargs):
        self.tickets_status = self.tickets_available > 0
        super().save(*args, **kwargs)

    def format_flight_info(self):
        return (
            f'{self.flight_number} \n'
            f'{self.city_from} -> {self.city_to}\n'
            f'{self.departure.strftime("%d.%m.%y в.%H:%M")}\n'
            f'{self.company}'
                )

class UserModel(AbstractUser):

    city = models.CharField(max_length=64, blank=True)
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions', blank=True)

    class Meta:
        db_table = 'user_table'

    def __str__(self):
        return self.first_name or self.username

class TicketsModel(models.Model):
    ticket_number = models.CharField(max_length=9, unique=True)
    flight = models.ForeignKey(FlightModel, related_name='tickets', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    owner = models.ForeignKey(UserModel, related_name='tickets', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'tickets_table'

    def __str__(self):
        return self.ticket_number

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            prefix = (
                (self.flight.company[0] if self.flight.company else 'X').upper() +
                (self.flight.city_from[0] if self.flight.city_from else 'X').upper() +
                (self.flight.city_to[0] if self.flight.city_to else 'X').upper()
            )
            while True:
                digits = ''.join(random.choices(string.digits, k=6))
                candidate = f'{prefix}{digits}'
                if not TicketsModel.objects.filter(ticket_number=candidate).exists():
                    self.ticket_number = candidate
                    break
        super().save(*args, **kwargs)