from django.conf import settings
from shopify_app.config import DEFAULTS

from shopify_app.decorators import shop_login_required
from shopify_app.views.shop import PreferencesView

from extended_app.services.extended_shop_service import ExtendedShopService

class PreferencesView(PreferencesView):
    """
        Main View to access the shop account
    """
    service = ExtendedShopService()

