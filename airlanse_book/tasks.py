from celery import shared_task
from .services.pdf_gen import send_ticket_email
from django.utils import timezone
from .models import FlightModel, TicketsModel



@shared_task
def send_ticket_email_task(ticket_id):
    send_ticket_email(ticket_id)

@shared_task
def archive_flights():
    now = timezone.now()
    flights_to_archive = (
            FlightModel.objects.filter(is_archived=False, tickets_status=False) |
            FlightModel.objects.filter(is_archived=False, departure__lte=now)
    )
    flights_to_archive.update(is_archived=True)

