from base import BaseService
from django.conf import settings

from shopify_app.models import Shop
from shopify_app.utils.python import normalize_url
from shopify_app.config import DEFAULTS

from shopify_service import ShopifyService
from config_service import ConfigService
from plan_service import PlanService
from plan_config_service import PlanConfigService


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

        shopify_service = ShopifyService(token=token, domain=domain)
        shop = shopify_service.Shop.current()
        shop_model, created = self.get_or_create(shop_id=shop.id)

        for field in shop_model.update_fields():
            setattr(shop_model, field, shop.attributes.get(field))

        shop_model.token = token
        shop_model.save()

        redirect_url = False
        if not self._check_active_plan(shop_model):
            redirect_url = self.get_upgrade_plan_url(shopify_service, shop_model)

        self.post_install(request)

        return shop_model, redirect_url

    def _check_active_plan(self, shop):

        if not ConfigService().is_active_billing():
            return True

        current_plan = shop.current_plan()
        if not current_plan:
            return False
        else:
            return ShopifyService(shop_model).is_active_charge(current_plan.charge_id)

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

    def get_upgrade_plan_url(self, shopify_service, shop):
        """
            Creates the shop plan and returns the confirmation url where
            the user should accept the billing.
        """

        if not ConfigService().is_active_billing():
            return False

        config = ConfigService().get_config()
        plan_config = config.plan_config
        import ipdb
        ipdb.set_trace()
        
        data = {
            "name": plan_config.name if plan_config else "Default",
            "price": plan_config.billing_amount if plan_config else "10.0",
            "trial_days": plan_config.trial_period_days if plan_config else 15,
            "return_url": "%s/shop/billing/?shop=%s&plan_config=%s" % (getattr(settings, "HOST", DEFAULTS["HOST"]), shop.id, plan_config.id),
        }

        if getattr(settings, "TEST", True):
            data["test"] = True
        
        response = shopify_service.RecurringApplicationCharge.create(data)
        response_data = response.to_dict()

        if response.errors.errors:
            raise Exception(str(response.errors.errors))

        return response_data["confirmation_url"]

    def upgrade_plan(self, shop_id, plan_config_id, charge_id):

        shop_model = self.get(id=shop_id)

        plan = PlanService().new(shop=shop_model)
        plan_config = PlanConfigService().get(id=plan_config_id)

        for field in plan_config.update_fields():
            setattr(plan, field, getattr(plan_config, field, ""))

        plan.charge_id = charge_id
        plan.save()
