from base import BaseService
from django.conf import settings

from shopify_app.models import Shop
from shopify_app.utils.python import normalize_url

from shopify_service import ShopifyService
from config_service import ConfigService
from plan_service import PlanService


class ShopService(BaseService):

    entity = Shop

    def install(self, request):
        """
            Installation / app preferences service handler.

            Creates a new store object if it doesn't exists with
            all the shopify API shop attributes.
        """

        self.before_install(request)

        token = request.session.get('shopify', {}).get("access_token")
        domain = request.session.get('shopify', {}).get("shop_url")
        
        shop = ShopifyService(token=token, domain=domain).Shop.current()
        shop_model, created = self.get_or_create(shop_id=shop.id)

        for field in shop_model.update_fields():
            setattr(shop_model, field, shop.attributes.get(field))

        shop_model.token = token
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

        plan_config = config.plan_config
        if plan_config is None or not plan_config.enable_billing:
            return False

        data = {
            "name": plan_config.name,
            "price": plan_config.billing_amount,
            "trial_days": plan_config.trial_period_days,
            "return_url": "%s%s" % (settings.HOST, "/shop/billing/"),
        }

        if settings.TEST:
            data["test"] = True
        
        response = ShopifyService().RecurringApplicationCharge.create(data)
        response_data = response.to_dict()

        plan = PlanService().new(shop=shop)
        for field in plan_config.update_fields():
            setattr(plan, field, getattr(plan_config, field, ""))

        plan.save()

        return response_data["confirmation_url"]