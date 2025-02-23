from celery import shared_task
try:
    from recruitment.models import JobApplication
except ImportError:
    JobApplication = None  # ✅ Prevents import error if recruitment is not installed
    
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email_task(email, subject, message):  # ✅ Added message parameter
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    return f"Email sent to {email}"

@shared_task
def test_task():
    return "Celery is working!"


@shared_task
def process_pending_applications():
    if JobApplication is None:  # ✅ Prevents NoneType errors
        return "JobApplication model is not available."

    pending_apps = JobApplication.objects.filter(status="pending")

    for app in pending_apps:
        print(f"Processing application for {app.applicant_name}")
        app.status = "under_review"
        app.save()

    return f"Processed {pending_apps.count()} applications"
