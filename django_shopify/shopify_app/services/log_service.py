from base import BaseService
from shopify_app.models import RequestLog


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
