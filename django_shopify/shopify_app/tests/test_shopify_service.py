import simplejson as json
from django.test import TestCase

from django.conf import settings
from django.utils.importlib import import_module
from shopify_app.services import ShopifyService


class ShopifyServiceTest(TestCase):

    def test_get_all_customers(self):

        objs = ShopifyService(token=settings.SHOPIFY_TEST_PASSWORD, domain=settings.SHOPIFY_TEST_HOST).Customer.find()

        self.assertEquals(type(objs), list)
        self.assertEquals(len(objs), 1)

        self.assertEquals(objs[0].attributes["first_name"], "test")
        self.assertEquals(objs[0].attributes["last_name"], "test")
        self.assertEquals(objs[0].attributes["email"], "test@test.com")

    def test_create_product(self):

        data = {
            "title": "test",
            "body_html": "<strong>test</strong>",
            "vendor": "test",
            "product_type": "test",
            "tags": "test"
        }        

        product = ShopifyService(token=settings.SHOPIFY_TEST_PASSWORD, domain=settings.SHOPIFY_TEST_HOST).Product.create(data)

        self.assertEquals(type(product.id), int)

        for key, value in data.iteritems():
            self.assertEquals(product.attributes[key], value)

    def test_delete_products(self):

        products = ShopifyService(token=settings.SHOPIFY_TEST_PASSWORD, domain=settings.SHOPIFY_TEST_HOST).Product.find()

        for product in products:            
            product.destroy()

        products = ShopifyService(token=settings.SHOPIFY_TEST_PASSWORD, domain=settings.SHOPIFY_TEST_HOST).Product.find()

        self.assertEquals(products, [])