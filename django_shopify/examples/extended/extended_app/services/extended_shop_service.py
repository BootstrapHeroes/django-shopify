from extended_app.models import ExtendedShop
from shopify_app.services.shop_service import ShopService

class ExtendedShopService(ShopService):

    entity = ExtendedShop

    def before_save(self, shop_model, request):
        shop_model.is_enabled = True
        shop_model.has_products = True
