import importlib
from django.conf import settings

from shopify_app.services.shop_service import ShopService


def import_shop_service():

    shop_service_class_name = getattr(settings, "SHOP_SERVICE", None)
    if shop_service_class_name is None:
        return ShopService()

    shop_service_class_parts = shop_service_class_name.split(".")
    shop_service_pkg = ".".join(shop_service_class_parts[0:-1])

    shop_service_module = importlib.import_module(shop_service_pkg)
    shop_service_class = getattr(shop_service_module, shop_service_class_parts[-1])

    return shop_service_class()
