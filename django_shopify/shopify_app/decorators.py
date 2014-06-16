from django.shortcuts import redirect
from django.conf import settings
from shopify_app.services.shopify_api import APIWrapper
from shopify_app.utils.importer import import_shop_service


def shop_login_required(func):

    def wrapper(view, request, *args, **kwargs):

        if not settings.SHOPIFY_API_KEY or not settings.SHOPIFY_API_SECRET:
            raise Exception("SHOPIFY_API_KEY and SHOPIFY_API_SECRET must be set in settings")

        if hasattr(request, 'session') and 'shopify' in request.session:

            #Check if the app was uninstalled
            shop_service = import_shop_service()

            token = request.session["shopify"]["access_token"]
            shop_url = request.session["shopify"]["shop_url"]

            if not shop_service.is_valid_token(token, shop_url):

                request.session.pop("shopify", None)
                return redirect("/oauth/login/?error=invalid token")
        else:
            request.session['return_to'] = request.get_full_path()
            return redirect("/oauth/login/?error=must login first")

        return func(view, request, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
