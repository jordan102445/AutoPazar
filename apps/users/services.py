from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tasks import send_transactional_email


def send_verification_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verification_path = reverse("users:verify-email", kwargs={"uidb64": uid, "token": token})
    verification_url = request.build_absolute_uri(verification_path)

    subject = "Потврда на е-пошта"
    body = render_to_string(
        "emails/verify_email.txt",
        {
            "user": user,
            "verification_url": verification_url,
            "site_name": "AutoPazar",
            "site_url": settings.SITE_URL,
        },
    )
    send_transactional_email.delay(subject, body, [user.email])
