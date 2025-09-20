from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from .models import Task

def deadline_reminder():
    today = now().date()
    tasks = Task.objects.filter(due_date=today, status="Pending")

    for task in tasks:
        send_mail(
            subject="Task Deadline Reminder",
            message=f"Hello {task.assigned_to.name},\n\nYour task '{task.title}' is due today!\nPlease complete it on time.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[task.assigned_to.email],
            fail_silently=False,
        )
