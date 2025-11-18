import logging
from typing import Iterable

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


def _get_default_from_email() -> str:
    return getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "EMAIL_HOST_USER", "") or "no-reply@ngangi.local"


def send_member_approval_email(member) -> bool:
    """Send an automatic email to a member when their account is approved."""
    to_email = member.email or getattr(member.user, "email", None)
    if not to_email:
        logger.info("Skipping approval email for member %s – no email address.", member)
        return False

    context = {
        "member": member,
        "site_url": getattr(settings, "SITE_URL", "http://127.0.0.1:8000"),
    }
    subject = "Your Ngangi Platform membership has been approved"
    text_body = render_to_string("emails/member_approved_email.txt", context)
    html_body = render_to_string("emails/member_approved_email.html", context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=_get_default_from_email(),
        to=[to_email],
    )
    if html_body:
        email.attach_alternative(html_body, "text/html")

    try:
        email.send(fail_silently=False)
        return True
    except Exception as exc:  # pragma: no cover - logging for operational visibility
        logger.exception("Failed to send approval email to %s: %s", to_email, exc)
        return False


def send_group_notification_email(subject: str, message: str, members: Iterable) -> int:
    """Send a group notification email to the provided members. Returns number of emails attempted."""
    emails = []
    for member in members:
        email_address = member.email or getattr(member.user, "email", None)
        if email_address:
            emails.append(email_address)

    # Remove duplicates while preserving order
    seen = set()
    unique_emails = [email for email in emails if not (email in seen or seen.add(email))]

    if not unique_emails:
        logger.info("No email addresses found for group notification.")
        return 0

    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=_get_default_from_email(),
        bcc=unique_emails,
    )

    try:
        email.send(fail_silently=False)
        return len(unique_emails)
    except Exception as exc:  # pragma: no cover
        logger.exception("Failed to send group notification email: %s", exc)
        return 0


