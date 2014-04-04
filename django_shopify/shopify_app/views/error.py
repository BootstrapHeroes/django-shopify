import time

from shopify_upsell_app.services.log import LogService

from django.http import HttpResponseServerError
from shopify_upsell_app.utils.email import send_html_email

from django.conf import settings


def handler500(request):

    log = LogService().log_error(request)

    subject = "An error happened with id %s" % log.id
    sender = getattr(settings.SENDER_EMAIL)
    receiver = getattr(settings.SEND_ERROR_EMAIL)
    send_html_email(subject, log.stack_trace, sender, receiver)

    return HttpResponseServerError("<h1>500. Ups... An error ocurred</h1>")