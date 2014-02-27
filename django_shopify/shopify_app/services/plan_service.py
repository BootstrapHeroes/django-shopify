from base import BaseService
from shopify_app.models import Plan
from shopify_service import ShopifyService


class PlanService(BaseService):

    entity = Plan

    def is_active_plan(self, plan):
        """
            Returns if the plan is active or not.
        """

        if plan.uninstalled_at is not None:
            return False

        if plan.billing_type == "O":
            return ShopifyService(shop=plan.shop).is_active_charge(plan.charge_id)

        return ShopifyService(shop=plan.shop).is_active_recurring_charge(plan.charge_id)
