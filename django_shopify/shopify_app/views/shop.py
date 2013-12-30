from base import BaseView
from django.conf import settings

from shopify_app.decorators import shop_login_required
from shopify_app.services.shop_service import ShopService


class IndexView(BaseView):

    def get(self, *args, **kwargs):

        return self.redirect("/shop/preferences")


class PreferencesView(BaseView):
    """
        Main View to access the shop account
    """

    service = ShopService()
    
    @shop_login_required
    def get(self, *args, **kwargs):

        shop, redirect_url = self.service.install(self.request)

        if not redirect_url:
            redirect_url = settings.OAUTH_REDIRECT_URL

        return self.redirect(redirect_url)


class BillingView(BaseView):
    """
        Return handler for when a user accepts the billing plan for the app
    """

    @shop_login_required    
    def get(self, *args, **kwargs):

        return self.redirect(settings.BILLING_REDIRECT_URL)