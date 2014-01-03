from base import BaseService
from shopify_app.models import Plan
from shopify_service import ShopifyService

class PlanService(BaseService):

    entity = Plan

    def is_active_plan(self, plan):
    	if plan.billing_type == "O":
    		return ShopifyService(shop=plan.shop).is_active_charge(plan.charge_id)
    	else:
    		return ShopifyService(shop=plan.shop).is_active_recurring_charge(plan.charge_id)
