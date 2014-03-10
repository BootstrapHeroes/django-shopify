import time

from django.conf.urls import handler500 as django_handler500
from shopify_upsell_app.services.log import LogService
from shopify_app.views.base import BaseView

from django.http import HttpResponseServerError, HttpResponse


def handler500(request):

    LogService().log_error(request)
    
    return HttpResponseServerError("<h1>500. Ups... An error ocurred</h1>")


class Simulate500View(BaseView):

    def get(self, *args, **kwargs):

        #simulate a 500 error (global name 'undefined_variable' is not defined)
        undefined_variable

        return self.response("ok")


class SimulateTimeoutView(BaseView):

    def get(self, *args, **kwargs):

        #simulate a timeout error
        time.sleep(180)

        return self.response("ok")