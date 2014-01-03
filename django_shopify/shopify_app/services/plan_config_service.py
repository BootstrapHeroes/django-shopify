from base import BaseService
from shopify_app.models import PlanConfig
from django.conf import settings
from shopify_app.config import DEFAULTS


class PlanConfigService(BaseService):

    entity = PlanConfig

    def _get_charge_common_data(self, shop, plan_config):

        data = {
            "name": plan_config.name if plan_config.name else "Default",
            "price": plan_config.billing_amount if plan_config.billing_amount else "10.0",            
            "return_url": "%s/shop/billing/?shop=%s&plan_config=%s" % (getattr(settings, "HOST", DEFAULTS["HOST"]), shop.id, plan_config.id),
        }

        if getattr(settings, "TEST", True):
            data["test"] = True

        return data

    def one_time_charge(self, shopify_service, shop, plan_config):

        data = self._get_charge_common_data(shop, plan_config)

        return shopify_service.ApplicationCharge.create(data)

    def recurring_charge(self, shopify_service, shop, plan_config):

        data = self._get_charge_common_data(shop, plan_config)
        data["trial_days"] = plan_config.trial_period_days if plan_config.trial_period_days else 15
        
        return shopify_service.RecurringApplicationCharge.create(data)

    def confirm_data(self, shopify_service, shop, plan_config):
    	if plan_config.billing_type == "O":
            response = self.one_time_charge(shopify_service, shop, plan_config)
        else:
            response = self.recurring_charge(shopify_service, shop, plan_config)

        response_data = response.to_dict()

        if response.errors.errors:
            raise Exception(str(response.errors.errors))

        return response_data