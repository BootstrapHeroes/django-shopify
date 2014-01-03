from django.contrib import admin
from extended_app.models import ExtendedShop

class BaseAdmin(admin.ModelAdmin):

    exclude = ["created_at", "updated_at"]

admin.site.register(ExtendedShop, BaseAdmin)
