from shopify_app.views.base import BaseView
from shopify_app.services import ShopifyService


class IndexView(BaseView):

    url = r"^$"

    def get(self, *args, **kwargs):

        context = {{"PROJECT_VERSION": "0.0.1"}}

        try:
            context["shop"] = ShopifyService().Shop.current()
        except:
            pass

        return self.render_to_response(context)
