from django.test import TestCase

from django.conf import settings
from shopify_app.services import ShopService
from shopify_app.services import ShopifyService

from django.core.handlers.base import BaseHandler
from django.test.client import RequestFactory
 
class RequestMock(RequestFactory):

    def request(self, **request):

        "Construct a generic request object."
        request = RequestFactory.request(self, **request)
        handler = BaseHandler()
        handler.load_middleware()
        for middleware_method in handler._request_middleware:
            if middleware_method(request):
                raise Exception("Couldn't create request mock object - "
                                "request middleware returned a response")
        return request

    session = {}


class ShopServiceTest(TestCase):

    def setUp(self):

        self.request = RequestMock()
        self.request.session["shopify"] = {"access_token": ""}

    def test_shop_install(self):
        
        shop, redirect_url = ShopService().install(self.request)

        self.assertTrue(shop.id is not None)
        self.assertTrue(redirect_url is False)
        