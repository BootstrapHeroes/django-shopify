from base import BaseView
from settings import HOST, SHOPIFY_API_SCOPE
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Context
from django.core.urlresolvers import reverse
import shopify


class BaseOauthView(BaseView):
    """
        Base class of Aouth Flow Views. Provides common methods
    """
    
    def _return_address(self, request):
        """
            Return the return address stored on session or default
        """
        #FIXME Change store/preferences
        return request.session.pop('return_to', "/store/preferences/")


class LoginView(BaseOauthView):
    """
        Initial login action which ask user for their ${shop}.myshopify.com address and redirect user to shopify auth page
    """

    def get(self, *args, **kwargs):

        #If the ${shop}.myshopify.com address is already provided in the URL, just skip to authenticate
        if self.request.REQUEST.get('shop'):
            permission_url = shopify.Session.create_permission_url(shop.strip(), SHOPIFY_API_SCOPE)
            return redirect(permission_url)

        return super(BaseOauthView, self).get(*args, **kwargs)


class FinalizeView(BaseOauthView):
    """
        Finalize login action which receives the request from shopify and login the user to our app.
    """

    def get(self, *args, **kwargs):

        shop_url = self.request.REQUEST.get('shop')

        # Checking if the user has a previous valid session initialized, not need to initialize again
        if hasattr(self.request, 'session') and 'shopify' in self.request.session and self.request.session["shopify"]["shop_url"] == shop_url:
            return redirect("/store/preferences")

        # Initializing shopify session
        try:
            shopify_session = shopify.Session(shop_url)
            shopify_session.request_token(self.request.GET["code"])
        except:
            #Shopify session fails, redirect to login initial step
            return redirect("%s?shop=%s"%('/oauth/login', shop_url))


        # Store shopify sesssion data in our session
        self.request.session['shopify'] = {
                    "shop_url": shop_url,
                    "access_token": shopify_session.token,
                }

        response = redirect(self._return_address(self.request))
        return response