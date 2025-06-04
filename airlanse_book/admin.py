from django.contrib import admin
from .models import UserModel,FlightModel,TicketsModel

# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number','flight_status')
    list_per_page = 20


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','id','email')
    list_per_page = 20


class TicketsAdmin(admin.ModelAdmin):
    list_display = ('ticket_number',)
    search_fields = ['ticket_number']
    list_per_page = 20

admin.site.register(FlightModel, FlightAdmin)
admin.site.register(UserModel, UserAdmin)
admin.site.register(TicketsModel, TicketsAdmin)