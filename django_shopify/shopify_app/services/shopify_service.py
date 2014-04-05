try:
    import shopify
except ImportError:
    pass

from django.conf import settings

from shopify_api import APIWrapper
from shopify_app.utils.python import normalize_url


class ShopifyService(object):
    """
        @Deprecated. Please use services.shopify_api.APIWrapper to make
        requests to the shopify api.
    """

    #Set to True to force public app
    public_app = False

    def __new__(cls, *args, **kwargs):
        """
            Singleton class
        """
        if not hasattr(cls, "_instance"):
            cls._instance = super(ShopifyService, cls).__new__(cls)
        return cls._instance

    def _init_public_app(self, token, domain):
        """
            Initializes the shopify api client with the key of the shop
        """

        try:
            session = shopify.Session(domain)
            session.token = token
            return session
        except AttributeError:
            raise Exception("You have to specify the token and domain to init a public app")

    def _init_private_app(self):
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
        return session

    def __init__(self, token=None, domain=None, shop=None):

        if getattr(settings, "PUBLIC_APP", False) or self.public_app:

            if shop:
                token = shop.token
                domain = shop.myshopify_domain

            session = self._init_public_app(token, domain)

        else:
            session = self._init_private_app()

        shopify.ShopifyResource.activate_session(session)
        self.session = session
        self.shop = shop

    def __getattr__(self, name):
        """
            Delegates all the undefined methods and attributes to the shopify client.
        """

        return getattr(shopify, name)

    def is_active_charge(self, charge_id):

        charge = APIWrapper(self.shop).get("application_charge", charge_id)
        return charge and charge["status"] == "active"

    def is_active_recurring_charge(self, charge_id):

        charge = APIWrapper(self.shop).get("recurring_application_charge", charge_id)
        return charge and charge["status"] == "active"
