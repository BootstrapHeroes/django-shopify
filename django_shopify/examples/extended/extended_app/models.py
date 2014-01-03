from django.db import models

from shopify_app.models import Shop
from django.contrib.auth.models import User


class ExtendedShop(Shop):
    """
        This is an example of how to use inheritance to add attributes to the 
        default Shop model.
    """

    is_enabled = models.BooleanField(default=False)
    has_products = models.BooleanField(default=True)


class Project(models.Model):
    """
        This is an example of how to use ForeignKeys to the default Shop model.
    """

    shop = models.ForeignKey(Shop)
    user = models.ForeignKey(User)
