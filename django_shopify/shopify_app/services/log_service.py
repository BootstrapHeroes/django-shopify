import sys
from datetime import datetime
from django.views.debug import ExceptionReporter

from base import BaseService
from shopify_app.models import RequestLog, ErrorLog


class LogService(BaseService):

    entity = RequestLog

    def log_request(self, request):

        data = {
            "url": request.get_full_path(),
            "headers": str(request.META),
            "payload": request.body,
            "method": request.method,
        }

        data["params"] = str(request.REQUEST)

        log = self.new(**data)
        log.save()

    def log_shopify_request(self, url, method="get", params=None, response=None):

        data = {
            "url": url,
            "method": method,
        }

        if response:
            data["response"] = response

        if params:
            data["params"] = str(params)

        log = self.new(**data)
        log.save()

    def log_error(self, request):

        etype, evalue, etraceback = sys.exc_info()
        sys.exc_clear()

        stack_trace = ExceptionReporter(request, etype, evalue, etraceback).get_traceback_text()

        data = {
            "page_url": request.get_full_path(),
            "params": str(request.REQUEST),
            "headers": str(request.META),
            "stack_trace": stack_trace,
            "datetime": datetime.now(),
        }

        log = ErrorLog(**data)
        log.save()

        return log