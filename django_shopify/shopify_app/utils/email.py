from django.core.mail import EmailMultiAlternatives
from threading import Thread


def send_html_email(subject, content, from_email, to_email, fail_silently=False, bcc=[]):

    if not isinstance(to_email, list):
        to_email = [to_email]

    msg = EmailMultiAlternatives(subject=subject, body=content, from_email=from_email, to=to_email, bcc=bcc)
    msg.attach_alternative(content, "text/html")

    thread = Thread(target=lambda: msg.send(fail_silently=fail_silently))
    thread.start()