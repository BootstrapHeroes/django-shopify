from base import BaseService
from shopify_app.models import RequestLog


class LogService(BaseService):

	entity = RequestLog

	def log_request(self, request):

		data = {
            "url": request.get_full_path(), 
            "params": str(request.REQUEST), 
            "headers": str(request.META), 
        }

        log = self.new(**data)
        log.save()
