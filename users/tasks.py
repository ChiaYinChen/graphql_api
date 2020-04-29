"""Celery tasks."""
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

from graphql_api.settings import DOMAIN, EMAIL_HOST_USER


@shared_task
def send_confirmation_email(email, username):
    """Send confirmation email."""
    context = {
        'small_text_detail': 'Thank you for '
                             'creating an account. '
                             'Please verify your email '
                             'address to set up your account.',
        'username': username,
        'email': email,
        'domain': DOMAIN
    }
    html_message = render_to_string('email.html', context)
    mail_sent = send_mail(
        subject='Email Verification',
        message='',
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
        html_message=html_message
    )
    return mail_sent
