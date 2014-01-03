from extended_app.models import ExtendedShop
from shopify_app.services.shop_service import ShopService

class ExtendedShopService(ShopService):

    entity = ExtendedShop
