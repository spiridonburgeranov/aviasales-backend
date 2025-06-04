from django.db import transaction
from django.core.exceptions import ValidationError
from airlanse_book.models import TicketsModel, FlightModel, UserModel, FlightStatusModel


def purchase_ticket(flight: FlightModel, user: UserModel) -> TicketsModel:
    with transaction.atomic():
        flight = FlightModel.objects.select_for_update().get(id=flight.id)
        if flight.tickets_available <= 0:
            raise ValidationError('Нет доступных билетов на данный рейс')
        ticket = TicketsModel.objects.create(
            flight=flight,
            price=flight.ticket_price,
            owner=user
        )
        flight.tickets_available -= 1
        if flight.tickets_available == 0:
            flight.flight_status = FlightStatusModel.CHECK_IN_CLOSED
        flight.save()
        return ticket