from django.contrib import admin
from shopify_app.models import Config


class ConfigAdmin(admin.ModelAdmin):

    exclude = ["created_at", "updated_at"]


admin.site.register(Config, ConfigAdmin)