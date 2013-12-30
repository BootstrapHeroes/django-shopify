from base import BaseView
from django.conf import settings

from shopify_app.decorators import shop_login_required
from shopify_app.services.shop_service import ShopService


class IndexView(BaseView):

    def get(self, *args, **kwargs):

        return self.redirect("/shop/preferences")

class PreferencesView(BaseView):
    """
        Main View to access the shop account
    """
    
    @shop_login_required    
    def get(self, *args, **kwargs):

        ShopService().install(self.request)
        return self.redirect("/")
