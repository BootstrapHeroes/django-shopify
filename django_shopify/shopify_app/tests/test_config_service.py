from django.test import TestCase

from django.conf import settings
from shopify_app.services import ConfigService


class ShopServiceTest(TestCase):

    def test_shop_install(self):

        config = ConfigService().get_config()
        self.assertEquals(config.id, 1)

    def test_billing_disabled_by_default(self):

        self.assertEquals(ConfigService().is_active_billing(), False)