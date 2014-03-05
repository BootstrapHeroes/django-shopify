from base import BaseService
from shopify_app.models import RequestLog


class LogService(BaseService):

    entity = RequestLog

    def log_request(self, request):

        data = {
            "url": request.get_full_path(),  
            "headers": str(request.META), 
            "payload": request.body,
        }

        if request.method == "GET":
            data["get"] = str(request.GET)
        else:
            data["post"] = str(request.POST)

        log = self.new(**data)      
        log.save()

    def log_shopify_request(self, url, method="get", params=None, response=None):

        data = {
            "url": url,
        }

        if response:
            data["response"] = response

        if params:
            if method == "get":
                params["get"] = str(params) 
            else:
                params["post"] = str(params)

        log = self.new(**data)      
        log.save()