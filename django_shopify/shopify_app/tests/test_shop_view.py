from django_webtest import WebTest
from django.conf import settings
from django.utils.importlib import import_module
from shopify_app.models import Shop
from shopify_app.services import ConfigService

class ShopView(WebTest):

    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

        shop = Shop.objects.filter(myshopify_domain=settings.SHOPIFY_TEST_HOST)
        if shop:
        	shop.delete()

    def test_not_logged_preferences(self):
        response = self.app.get('/shop/preferences/')

        assert response.status_code == 302
        assert '/oauth/login' in response.location
        #FIXME
        #self.assertRedirects(response, '/oauth/login', status_code=301)

    def test_install_preferences(self):

        session = self.client.session
        session["shopify"] = {
            "access_token": settings.SHOPIFY_TEST_PASSWORD,
            "shop_url": settings.SHOPIFY_TEST_HOST,
        }
        session.save()

        # pretend to be logged in as user `kmike` and go to the index page
        response = self.client.get('/shop/preferences/')

        assert response.status_code == 302
        assert Shop.objects.filter(myshopify_domain=settings.SHOPIFY_TEST_HOST).exists()

        # pretend to be logged in as user `kmike` and go to the index page
        response = self.client.get('/shop/preferences/')

        assert response.status_code == 302
        assert len(Shop.objects.filter(myshopify_domain=settings.SHOPIFY_TEST_HOST))== 1

    def test_install_with_payments(self):
        config = ConfigService().get_config()
        config.enable_billing = True
        config.save()

        session = self.client.session
        session["shopify"] = {
            "access_token": settings.SHOPIFY_TEST_PASSWORD,
            "shop_url": settings.SHOPIFY_TEST_HOST,
        }
        session.save()

        # pretend to be logged in as user `kmike` and go to the index page
        response = self.client.get('/shop/preferences/')

        assert response.status_code == 302
        assert "%s/admin/charges/"%settings.SHOPIFY_TEST_HOST in response["location"]
        assert Shop.objects.filter(myshopify_domain=settings.SHOPIFY_TEST_HOST).exists()        

        config.enable_billing = False
        config.save()
