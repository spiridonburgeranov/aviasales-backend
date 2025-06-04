from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TicketsModel
from .tasks import send_ticket_email_task
from django.db import transaction


@receiver(post_save, sender=TicketsModel)
def ticket_created_handler(sender, instance, created, **kwargs):
    if created:
        ticket_id = instance.id
        transaction.on_commit(lambda: send_ticket_email_task.delay(ticket_id))