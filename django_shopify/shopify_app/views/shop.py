from base import BaseView
from django.conf import settings
from shopify_app.config import DEFAULTS

from shopify_app.utils.importer import import_shop_service
from shopify_app.decorators import shop_login_required
from shopify_app.services.shop_service import ShopService
from shopify_app.services.log_service import LogService


class BaseShopView(BaseView):

    service = import_shop_service()


class IndexView(BaseShopView):

    def get(self, *args, **kwargs):

        return self.redirect(getattr(settings, "PREFERENCES_URL", DEFAULTS["PREFERENCES_URL"]))


class PreferencesView(BaseShopView):
    """
        Main View to access the shop account
    """

    @shop_login_required
    def get(self, *args, **kwargs):

        LogService().log_request(self.request)

        shop, redirect_url = self.service.install(self.request)
        self.request.session["shop"] = shop

        if not redirect_url:
            redirect_url = getattr(settings, "OAUTH_REDIRECT_URL", DEFAULTS["OAUTH_REDIRECT_URL"])

        return self.redirect(redirect_url)


class BillingView(BaseShopView):
    """
        Return handler for when a user accepts the billing plan for the app
    """

    @shop_login_required
    def get(self, *args, **kwargs):

        LogService().log_request(self.request)

        shop_id = self.request.GET.get("shop")
        plan_config_id = self.request.GET.get("plan_config")
        charge_id = self.request.GET.get("charge_id")

        if not ShopService().upgrade_plan(shop_id, plan_config_id, charge_id):
            return self.redirect(getattr(settings, "BILLING_DECLINE_REDIRECT_URL", DEFAULTS["BILLING_DECLINE_REDIRECT_URL"]))

        return self.redirect(getattr(settings, "BILLING_REDIRECT_URL", DEFAULTS["BILLING_REDIRECT_URL"]))
