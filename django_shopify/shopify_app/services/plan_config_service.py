from base import BaseService
from shopify_app.models import PlanConfig
from django.conf import settings
from shopify_app.config import DEFAULTS
from datetime import datetime

class PlanConfigService(BaseService):

    entity = PlanConfig

    def _get_charge_common_data(self, shop, plan_config):
        """
            Returns the common data for the charge API call
        """

        data = {
            "name": plan_config.name if plan_config.name else "Default",
            "price": plan_config.billing_amount if plan_config.billing_amount else "10.0",            
            "return_url": "%s/shop/billing/?shop=%s&plan_config=%s" % (getattr(settings, "HOST", DEFAULTS["HOST"]), shop.id, plan_config.id),
        }

        if getattr(settings, "TEST", True):
            data["test"] = True

        return data

    def one_time_charge(self, shopify_service, shop, plan_config):
        """
            Generates a one time charge for this app
        """

        data = self._get_charge_common_data(shop, plan_config)

        return shopify_service.ApplicationCharge.create(data)

    def recurring_charge(self, shopify_service, shop, plan_config):
        """
            Generates a recurring charge for this app
        """

        data = self._get_charge_common_data(shop, plan_config)
        default_trial_days = plan_config.trial_period_days if plan_config.trial_period_days else 15

        #trial days starts counting from the first install
        current_trial_days = (datetime.utcnow().replace(tzinfo=None) - shop.created_at.replace(tzinfo=None)).days
        if not current_trial_days >= default_trial_days:
            data["trial_days"] = default_trial_days - current_trial_days

        return shopify_service.RecurringApplicationCharge.create(data)

    def confirm_data(self, shopify_service, shop, plan_config):
        """
            Makes the request to Generate either a one time charge or recurring charge and
            returns the response results.

            If there are errors in the request response it raises an exception.
        """

    	if plan_config.billing_type == "O":
            response = self.one_time_charge(shopify_service, shop, plan_config)
        else:
            response = self.recurring_charge(shopify_service, shop, plan_config)

        response_data = response.to_dict()


        if response.errors.errors:
            raise Exception(str(response.errors.errors))

        return response_data