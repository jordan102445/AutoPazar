from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_transactional_email(subject, body, recipients):
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)

