from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings
import shopify

def shop_login_required(func):
    def wrapper(view, request, *args, **kwargs):

        if not hasattr(request, 'session') or 'shopify' not in request.session:
            request.session['return_to'] = request.get_full_path()
            return redirect("/oauth/login")

        if not settings.SHOPIFY_API_KEY or not settings.SHOPIFY_API_SECRET:
            raise ConfigurationError("SHOPIFY_API_KEY and SHOPIFY_API_SECRET must be set in settings")        
        
        shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY,
                              secret=settings.SHOPIFY_API_SECRET)

        if hasattr(request, 'session') and 'shopify' in request.session:
            shopify_session = shopify.Session(request.session['shopify']['shop_url'])
            shopify_session.token = request.session['shopify']['access_token']
            shopify.ShopifyResource.activate_session(shopify_session)
            request.session['shopify']["session"] = shopify_session

            try:
                request.session['shopify']["shop"] = shopify.Shop.current()
            except:
                request.session.pop("shopify")
                return redirect("/oauth/login")

        return func(view, request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
