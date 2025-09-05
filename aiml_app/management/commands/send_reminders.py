# send_reminders.py
import os
import django
from datetime import timedelta
from django.utils import timezone

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aiml_event.settings")
django.setup()

from aiml_app.models import Participant, Event
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

try:
    # Get the event
    event = Event.objects.get(slug="aiml-2025-paris")
    today = timezone.now().date()

    # 7 days reminder
    if today == event.start_date - timedelta(days=7):
        participants = Participant.objects.filter(paid=True)
        for p in participants:
            html_content = render_to_string("aiml_app/email_reminder.html", {"participant": p, "event": event})
            msg = EmailMultiAlternatives(
                subject="Reminder: AIML 2025",
                body=f"Dear {p.name}, Reminder: AIML 2025 is coming soon!",
                from_email="info@aiml-paris.com",
                to=[p.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    # Day-of event reminder (optional)
    if today == event.start_date:
        participants = Participant.objects.filter(paid=True)
        for p in participants:
            html_content = render_to_string("aiml_app/email_dayof.html", {"participant": p, "event": event})
            msg = EmailMultiAlternatives(
                subject="AIML 2025 Starts Today!",
                body=f"Dear {p.name}, AIML 2025 starts today at {event.location}.",
                from_email="info@aiml-paris.com",
                to=[p.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

except Event.DoesNotExist:
    print("Event not found.")
