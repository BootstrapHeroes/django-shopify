from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from settings import MEDIA_ROOT

from django_conventions import UrlsManager
import testapp_app.views as testapp_app_root

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True}),

    url(r'^', include('shopify_app.urls'), name='root_path'),

)

UrlsManager(urlpatterns, testapp_app_root)

handler500 = 'shopify_app.views.error.handler500'