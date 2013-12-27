import shopify
from django.conf import settings

from shopify_app.utils.python import normalize_url


class ShopifyService(object):

    def __init__(self):
        """
            Initializes the shopify api client with the keys stored in settings.py.
            SHOPIFY_API_KEY, SHOPIFY_API_SECRET, SHOPIFY_API_PASSWORD, and SHOPIFY_HOST
            must be defined in that file.
        """

        try:
            api_key = settings.SHOPIFY_API_KEY
            api_secret = settings.SHOPIFY_API_SECRET
            api_host = settings.SHOPIFY_HOST
            api_password = settings.SHOPIFY_API_PASSWORD
        except AttributeError:
            raise Exception("You have to specify the SHOPIFY_API_KEY, SHOPIFY_API_SECRET, SHOPIFY_API_PASSWORD, and SHOPIFY_HOST in settings.py")

        session = shopify.Session(normalize_url(api_host))
        session.token = api_password

        session.setup(api_key=api_key, secret=api_secret)

        shopify.ShopifyResource.activate_session(session)
        self.session = session

    def __getattr__(self, name):
        """
            Delegates all the undefined methods and attributes to the shopify client.
        """

        return getattr(shopify, name)