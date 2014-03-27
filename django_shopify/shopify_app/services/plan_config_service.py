from base import BaseService
from shopify_app.models import PlanConfig
from django.conf import settings
from shopify_app.config import DEFAULTS
from datetime import datetime
from shopify_api import APIWrapper


class PlanConfigService(BaseService):

    entity = PlanConfig

    def _get_charge_common_data(self, shop, plan_config):
        """
            Returns the common data for the charge API call
        """
        data = {
            "name": plan_config.name if plan_config.name else "Default",
            "price": plan_config.billing_amount if plan_config.billing_amount else 10.0,
            "return_url": "http:%s/shop/billing/?shop=%s&plan_config=%s" % (getattr(settings, "HOST", DEFAULTS["HOST"]), shop.id, plan_config.id),
        }

        if getattr(settings, "TEST", True):
            data["test"] = True

        return data

    def _create_charge(self, shop_model, api_entity, data):

        return APIWrapper(shop_model, log=True).create(api_entity, data)

    def one_time_charge(self, shop, plan_config):
        """
            Generates a one time charge for this app
        """

        data = self._get_charge_common_data(shop, plan_config)

        return self._create_charge(shop, "application_charge", data)

    def recurring_charge(self, shop, plan_config):
        """
            Generates a recurring charge for this app
        """

        data = self._get_charge_common_data(shop, plan_config)
        default_trial_days = plan_config.trial_period_days if plan_config.trial_period_days else 15

        #trial days starts counting from the first install
        current_trial_days = (datetime.utcnow().replace(tzinfo=None) - shop.created_at.replace(tzinfo=None)).days
        if not current_trial_days >= default_trial_days:
            data["trial_days"] = default_trial_days - current_trial_days

        return self._create_charge(shop, "recurring_application_charge", data)

    def confirm_data(self, shop, plan_config):
        """
            Makes the request to Generate either a one time charge or recurring charge and
            returns the response results.

            If there are errors in the request response it raises an exception.
        """

        if plan_config.billing_type == "O":
            response = self.one_time_charge(shop, plan_config)
        else:
            response = self.recurring_charge(shop, plan_config)

        if "errors" in response:
            raise Exception(str(response["errors"]))

        return response
