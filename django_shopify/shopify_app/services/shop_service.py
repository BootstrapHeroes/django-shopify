from base import BaseService
from shopify_app.models import Shop

from shopify_app.utils.python import normalize_url


class ShopService(BaseService):

    entity = Shop

    def install(self, request):
        """
            Installation / app preferences service handler.

            Creates a new store object if it doesn't exists with
            all the shopify API shop attributes.
        """

        self.before_install(request)

        shop = shopify.Shop.current()
        shop_model, created = self.get_or_create(shop_id=shop.id)

        for field in shop_model.fields():
            setattr(shop_model, field, shop.attributes.get(field))

        shop_model.token = request.session.get('shopify', {}).get("access_token")
        shop_model.shop_id = shop.id
        shop_model.save()

        self.post_install(request)

    def before_install(self, request):
        """
            Override this method and add behaviour on before install
        """

        pass

    def post_install(self, request):
        """
            Override this method and add behaviour on post install
        """

        pass