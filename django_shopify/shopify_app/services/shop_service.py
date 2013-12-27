from base import BaseService
from django.conf import settings

from shopify_app.models import Shop
from shopify_app.utils.python import normalize_url

from shopify_service import ShopifyService
from config_service import ConfigService


class ShopService(BaseService):

    entity = Shop

    def install(self, request):
        """
            Installation / app preferences service handler.

            Creates a new store object if it doesn't exists with
            all the shopify API shop attributes.
        """

        self.before_install(request)

        shop = ShopifyService().Shop.current()
        shop_model, created = self.get_or_create(shop_id=shop.id)

        for field in shop_model.fields():
            setattr(shop_model, field, shop.attributes.get(field))

        shop_model.token = request.session.get('shopify', {}).get("access_token")
        shop_model.shop_id = shop.id
        shop_model.save()

        self.post_install(request)

        return shop_model

    def before_install(self, request):
        """
            Override this method and add behaviour on before install
        """

        pass

    def post_install(self, request):
        """
            Override this method and add behaviour on post install
        """

        pass

    def create_plan(self, shop):
        """
            Creates the shop plan and returns the confirmation url where
            the user should accept the billing.
        """

        config = ConfigService().get_config()

        plan = config.plan
        if plan is None:
            return False

        data = {
            "name": plan.name,
            "price": plan.billing_amount,
            "trial_days": plan.trial_period_days,
            "return_url": "%s%s" % (settings.HOST, reverse("shopify_config.views.upgrade")),
        }

        if settings.TEST:
            data["test"] = True
        
        response = ShopifyService().RecurringApplicationCharge.create(data)
        response_data = response.to_dict()

        shop.plan = config.plan
        shop.save()

        return response_data["confirmation_url"]