from datetime import datetime
from django.db import models


class BaseEntity(models.Model):

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __init__(self, *args, **kwargs):

        now = datetime.now()
        kwargs.update(created_at=now, updated_at=now)
        models.Model.__init__(self, *args, **kwargs)

    def fields(self):

        return [key for key in self.__dict__.keys() if not key.startswith("_")]

    class Meta:
        abstract = True


class Shop(BaseEntity):

    shop_id = models.CharField(max_length=255, null=True, blank=True)
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

    current_plan = models.OneToOneField("Plan")


class Plan(BaseEntity):

    BILLING_INTERVAL = (
        ('D', 'Daily'),
        ('M', 'weekly'),
    )

    shop_id = models.ForeignKey("Shop")

    name = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)

    billing_amount = models.DecimalField(max_digits=15, decimal_places=4)
    billing_interval = models.CharField(max_length=2, null=True, blank=True, choices=BILLING_INTERVAL)

    trial_period_days = models.PositiveIntegerField(null=True, blank=True)
    planned_charge_date = models.DateTimeField(null=True, blank=True)


class Config(BaseEntity):

    BILLING_TYPE = (
        ('O', 'One Time'),
        ('I', 'Interval'),
    )

    enable_billing = models.BooleanField(default=False)
    billing_type = models.CharField(max_length=2, null=True, blank=True, choices=BILLING_TYPE)
    free_trial_enabled = models.BooleanField(default=False)
    free_trial_period = models.PositiveIntegerField(default=0)
    amount = models.DecimalField(max_digits=15, decimal_places=4)