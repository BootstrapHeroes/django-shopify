from base import BaseService

from shopify_app.models import Shop

from shopify_service import ShopifyService
from config_service import ConfigService
from plan_service import PlanService
from log_service import LogService
from shopify_api import APIWrapper
from plan_config_service import PlanConfigService
from datetime import datetime


class ShopService(BaseService):

    entity = Shop

    def get_shop_by_myshopify_domain(self, shop_url):

        return self.get_one(myshopify_domain=shop_url)

    def install(self, request):
        """
            Installation / app preferences service handler.

            Creates a new store object if it doesn't exists with
            all the shopify API shop attributes.
        """

        self.before_install(request)

        token = request.session.get('shopify', {}).get("access_token")
        domain = request.session.get('shopify', {}).get("shop_url")

        shop = APIWrapper(token=token, api_domain=domain, log=True).current_shop()
        shop_model, created = self.get_or_create(shop_id=shop["id"])

        for field in shop_model.update_fields():
            setattr(shop_model, field, shop.get(field))

        shop_model.token = token

        self.before_save(shop_model, request)

        shop_model.save()

        self.post_install(request)

        if not self._check_active_plan(shop_model):

            redirect_url = self.get_upgrade_plan_url(shop_model)
            LogService().log_shopify_request(redirect_url)

            return shop_model, redirect_url

        return shop_model, False

    def _check_active_plan(self, shop):
        """
            This method checks if the given shop has an active plan
            and return a boolean with the result
        """
        #Check if the payments are disabled, so in this case the plan is active (doesnt need one)
        if not ConfigService().is_active_billing():
            return True

        #Check if the user has a plan or if has an inactive plan
        current_plan = shop.current_plan()
        if not current_plan:
            return False

        return PlanService().is_active_plan(current_plan)

    def before_save(self, shop_model, request):
        """
            Override this method and add behaviour on before save shop
        """

        pass

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

    def get_upgrade_plan_url(self, shop):
        """
            Creates the shop plan and returns the confirmation url where
            the user should accept the billing.
        """

        if not ConfigService().is_active_billing():
            return False

        config = ConfigService().get_config()
        plan_config = config.plan_config
        response_data = PlanConfigService().confirm_data(shop, plan_config)

        return response_data["confirmation_url"]

    def find_app_charge(self, entity, shop_model, charge_id):

        return APIWrapper(shop_model, log=True).get(entity, charge_id)

    def activate_charge(self, entity, shop_model, charge_id):

        APIWrapper(shop_model, log=True).activate_charge(entity, charge_id)

    def upgrade_plan(self, shop_id, plan_config_id, charge_id):
        """
            Upgrades the plan for the current [shop_id] using the [plan_config_id].
            It also saved the [charge_id] on the plan model.
        """
        shop_model = self.get(id=shop_id)
        plan_config = PlanConfigService().get(id=plan_config_id)

        api_object = "application_charge" if plan_config.billing_type == "O" else "recurring_application_charge"
        charge = self.find_app_charge(api_object, shop_model, charge_id)

        if charge["status"] == "accepted":
            self.activate_charge(api_object, shop_model, charge["id"])
        elif charge["status"] == "declined":
            return False

        #Check if the charge is already activated
        charge = self.find_app_charge(api_object, shop_model, charge_id)

        if charge["status"] == "active":

            plan = PlanService().new(shop=shop_model)

            #copies all the attributes from the plan_config to the plan model
            for field in plan_config.update_fields():
                setattr(plan, field, getattr(plan_config, field, ""))

            plan.charge_id = charge_id
            plan.installed_at = datetime.utcnow()
            plan.save()
        else:
            return False

        return True
