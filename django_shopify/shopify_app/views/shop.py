from base import BaseView
from django.conf import settings
from shopify_app.config import DEFAULTS

from shopify_app.decorators import shop_login_required
from shopify_app.services.shop_service import ShopService


class BaseShopView(BaseView):

    service = ShopService()


class IndexView(BaseShopView):

    def get(self, *args, **kwargs):

        return self.redirect("/shop/preferences")


class PreferencesView(BaseShopView):
    """
        Main View to access the shop account
    """
    
    @shop_login_required    
    def get(self, *args, **kwargs):

        shop, redirect_url = self.service.install(self.request)

        if not redirect_url:
            redirect_url = getattr(settings, "OAUTH_REDIRECT_URL", DEFAULTS["OAUTH_REDIRECT_URL"])

        return self.redirect(redirect_url)


class BillingView(BaseShopView):
    """
        Return handler for when a user accepts the billing plan for the app
    """

    @shop_login_required    
    def get(self, *args, **kwargs):

        shop_id = self.request.GET.get("shop")
        plan_config_id = self.request.GET.get("plan_config")
        charge_id = self.request.GET.get("charge_id")
        
        ShopService().upgrade_plan(shop_id, plan_config_id, charge_id)

        return self.redirect(getattr(settings, "BILLING_REDIRECT_URL", DEFAULTS["BILLING_REDIRECT_URL"]))