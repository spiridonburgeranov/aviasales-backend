from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from airlanse_book.models import TicketsModel


def send_ticket_email(ticket_id):
    ticket = TicketsModel.objects.select_related('owner', 'flight').get(id=ticket_id)
    user_email = ticket.owner.email
    flight_info = ticket.flight.format_flight_info()
    ticket_number = ticket.ticket_number

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    margin = 20 * mm
    y = height - margin

    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, y, "Elektronnyy bilet")
    y -= 15 * mm

    p.setStrokeColorRGB(0.6, 0.6, 0.6)
    p.setLineWidth(1)
    p.line(margin, y, width - margin, y)
    y -= 10 * mm

    p.setFont("Helvetica", 12)
    p.drawString(margin, y, f"Nomer bileta: {ticket_number}")
    y -= 10 * mm
    p.drawString(margin, y, f"Flight info: {flight_info}")
    y -= 20 * mm

    p.showPage()
    p.save()
    buffer.seek(0)

    email = EmailMessage(
        subject='Vash bilet',
        body='Zdravstvuyte! Fayl vashego bileta mozhno nayti vo vlozhenii.\n'
             'Eto pismo generiruetsya avtomaticheski, otvechat na nego ne nuzhno.',
        to=[user_email]
    )
    email.attach(f'ticket_{ticket_id}.pdf', buffer.read(), 'application/pdf')
    email.send()
