from base import BaseView
from shopify_app.config import DEFAULTS
from django.conf import settings

from shopify_app.services.log_service import LogService
from shopify_app.services.shopify_api import APIWrapper
from shopify_app.services.shop_service import ShopService


class LoginView(BaseView):
    """
        Initial login action which ask user for their ${shop}.myshopify.com address and self.redirect user to shopify auth page
    """

    def get(self, *args, **kwargs):

        LogService().log_request(self.request)

        if hasattr(self.request, 'session') and 'shopify' in self.request.session:
            return self.redirect(getattr(settings, "PREFERENCES_URL", DEFAULTS["PREFERENCES_URL"]))

        #If the ${shop}.myshopify.com address is already provided in the URL, just skip to authenticate
        if self.request.REQUEST.get('shop'):

            shop = self.request.REQUEST.get('shop').strip()
            permission_url = APIWrapper(shop_url=shop).permissions_url()

            LogService().log_shopify_request(permission_url)

            return self.redirect(permission_url)

        return super(BaseOauthView, self).get(*args, **kwargs)


class FinalizeView(BaseView):
    """
        Finalize login action which receives the request from shopify and login the user to our app.
    """

    def get(self, *args, **kwargs):

        LogService().log_request(self.request)

        shop_url = self.request.REQUEST.get('shop')
        shop = ShopService().get_one(myshopify_domain=shop_url)

        if shop is None:
            #If shop doesn't exists get the permanent token using the API
            try:
                permanent_token = APIWrapper(shop_url=shop_url).permanent_token(self.request.GET["code"])
            except:
                #Shopify session fails, self.redirect to login initial step
                return self.redirect("%s?shop=%s" % ("/oauth/login", shop_url))
        else:
            permanent_token = shop.token

        # Store shopify sesssion data in our session
        self.request.session['shopify'] = {
            "shop_url": shop_url,
            "access_token": permanent_token,
        }

        return self.redirect(getattr(settings, "PREFERENCES_URL", DEFAULTS["PREFERENCES_URL"]))
