from django.conf.urls import patterns, include, url

from django_conventions import UrlsManager
import shopify_app.views as views_root

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

UrlsManager(urlpatterns, views_root)
