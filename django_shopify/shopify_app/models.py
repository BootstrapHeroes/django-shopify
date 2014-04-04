from datetime import datetime
from django.db import models


class BaseEntity(models.Model):

    NOT_IN_FIELDS = []

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __init__(self, *args, **kwargs):

        now = datetime.now()
        kwargs.update(created_at=now, updated_at=now)
        models.Model.__init__(self, *args, **kwargs)

    def fields(self):

        return [key for key in self.__dict__.keys() if not key.startswith("_")]

    def update_fields(self):

        return [field for field in self.fields() if field not in self.NOT_IN_FIELDS]

    class Meta:
        abstract = True


class Shop(BaseEntity):
    """
        Represents a Store with all the information stored on shopify API
    """
    shop_id = models.CharField(max_length=255, null=False, blank=False, unique=True)
    token = models.CharField(max_length=255, null=True, blank=True)

    address1 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    country_code = models.CharField(max_length=255, null=True, blank=True)
    country_name = models.CharField(max_length=255, null=True, blank=True)
    customer_email = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=255, null=True, blank=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    google_apps_domain = models.CharField(max_length=255, null=True, blank=True)
    google_apps_login_enabled = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    money_format = models.CharField(max_length=255, null=True, blank=True)
    money_with_currency_format = models.CharField(max_length=255, null=True, blank=True)
    myshopify_domain = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    plan_name = models.CharField(max_length=255, null=True, blank=True)
    display_plan_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    province_code = models.CharField(max_length=255, null=True, blank=True)
    public = models.CharField(max_length=255, null=True, blank=True)
    shop_owner = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    tax_shipping = models.CharField(max_length=255, null=True, blank=True)
    taxes_included = models.CharField(max_length=255, null=True, blank=True)
    county_taxes = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=255, null=True, blank=True)
    zip = models.CharField(max_length=255, null=True, blank=True)

    NOT_IN_FIELDS = ["id", "created_at", "updated_at", "shop_id", "token"]

    def current_plan(self):

        plans = self.plan_set.order_by("-id")
        if not plans:
            return

        return plans[0]

    def __unicode__(self):

        return "{0} - {1}".format(self.shop_id, self.domain)


class PlanAttributes(BaseEntity):
    """
        Represents the plan attributes needed to bill stores
    """
    BILLING_TYPE = (
        ('O', 'One Time'),
        ('I', 'Interval'),
    )

    name = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)

    billing_amount = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    billing_type = models.CharField(max_length=2, null=True, blank=True, choices=BILLING_TYPE)

    trial_period_days = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):

        return "{0} - ${1}".format(self.name, self.billing_amount)


class PlanConfig(PlanAttributes):
    """
        Represents the payments configuration for bill shops
    """
    NOT_IN_FIELDS = ["id", "created_at", "updated_at"]


class Plan(PlanAttributes):
    """
        Represents the agreement associated with a shop based on the plan attributes.
    """
    shop = models.ForeignKey("Shop")
    charge_id = models.CharField(max_length=255, null=False, blank=False)

    installed_at = models.DateTimeField(null=True, blank=True)
    uninstalled_at = models.DateTimeField(null=True, blank=True)


class Config(BaseEntity):
    """
        Represents the payment configuration for all shops specified by the admin.
    """
    enable_billing = models.BooleanField(default=False)

    plan_config = models.OneToOneField("PlanConfig", null=True, blank=True)

    def __unicode__(self):

        return "{0}".format(self.id)


class RequestLog(BaseEntity):

    url = models.CharField(max_length=1000, null=True, blank=True)
    headers = models.TextField(null=True, blank=True)
    method = models.CharField(max_length=20, null=True, blank=True)
    payload = models.TextField(null=True, blank=True)
    params = models.TextField(null=True, blank=True)

    response = models.TextField(null=True, blank=True)


class ErrorLog(models.Model):

    page_url = models.CharField(max_length=4000)
    params = models.CharField(max_length=4000)
    headers = models.CharField(max_length=4000)
    stack_trace = models.TextField()

    datetime = models.DateTimeField(default=None, null=True, blank=True)
