from django.contrib import admin
from shopify_app.models import Config, PlanConfig, Plan, Shop


class BaseAdmin(admin.ModelAdmin):

    exclude = ["created_at", "updated_at"]


admin.site.register(Config, BaseAdmin)
admin.site.register(PlanConfig, BaseAdmin)
admin.site.register(Plan, BaseAdmin)
admin.site.register(Shop, BaseAdmin)