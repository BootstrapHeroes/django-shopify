from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from settings import MEDIA_ROOT

from django_conventions import UrlsManager
import extended_app.views as extended_app_root

admin.autodiscover()

urlpatterns = []

UrlsManager(urlpatterns, extended_app_root)

urlpatterns = urlpatterns + patterns('',

    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True}),

    url(r'^', include('shopify_app.urls'), name='root_path'),

)
