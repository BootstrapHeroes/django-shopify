from django.contrib import admin
from shopify_app.models import Config, PlanConfig


class BaseAdmin(admin.ModelAdmin):

    exclude = ["created_at", "updated_at"]


admin.site.register(Config, BaseAdmin)
admin.site.register(PlanConfig, BaseAdmin)