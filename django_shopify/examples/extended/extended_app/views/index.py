from shopify_app.views.base import BaseView

from extended_app.models import ExtendedShop


class IndexView(BaseView):

    url = r"^$"

    def get(self, *args, **kwargs):

        context = {
            "shops": ExtendedShop.objects.all()
        }

        return self.render_to_response(context)
