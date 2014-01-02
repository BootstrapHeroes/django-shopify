from django.test import TestCase

from django.conf import settings
from shopify_app.services import ShopService
from shopify_app.services import ShopifyService
from shopify_app.services import ConfigService

from django.core.handlers.base import BaseHandler
from django.test.client import RequestFactory
 

class RequestMock(RequestFactory):

    session = {}

    def request(self, **request):
        """
            Construct a generic request object.
        """

        request = RequestFactory.request(self, **request)
        handler = BaseHandler()
        handler.load_middleware()
        for middleware_method in handler._request_middleware:
            if middleware_method(request):
                raise Exception("Couldn't create request mock object - request middleware returned a response")
        return request


class ShopServiceTest(TestCase):

    config_service = ConfigService()
    shopify_service = ShopifyService()

    def setUp(self):

        self.request = RequestMock()
        self.request.session["shopify"] = {
            "access_token": "c9ea03feb20b5aab04c95f421e0c96be",
            "shop_url": "http://sticky-local.myshopify.com",
        }

        self.shopify_service.public_app = True

    def set_billing(self, state):

        config = self.config_service.get_config()
        config.enable_billing = state
        config.save()

    def test_shop_install(self):

        self.set_billing(False)
        shop, redirect_url = ShopService().install(self.request)

        self.assertTrue(shop.id is not None)
        self.assertTrue(redirect_url is False)
        
    def test_shop_billing_install(self):
        
        self.set_billing(True)
        shop, redirect_url = ShopService().install(self.request)

        self.assertTrue(shop.id is not None)
        self.assertTrue(isinstance(redirect_url, basestring))

    def tearDown(self):

        self.shopify_service.public_app = False