import time

from shopify_app.services.log_service import LogService
from shopify_app.config import DEFAULTS

from django.http import HttpResponseServerError
from shopify_app.utils.email import send_html_email

from django.conf import settings


def handler500(request):

    log = LogService().log_error(request)

    subject = "An error happened with id %s" % log.id

    sender = getattr(settings, "ERROR_EMAIL_SENDER", DEFAULTS["ERROR_EMAIL_SENDER"])
    receiver = getattr(settings, "ERROR_EMAIL_RECEIVER", DEFAULTS["ERROR_EMAIL_RECEIVER"])

    if sender is not None and receiver is not None:
        send_html_email(subject, log.stack_trace, sender, receiver)

    return HttpResponseServerError("<h1>500. Ups... An error ocurred</h1>")