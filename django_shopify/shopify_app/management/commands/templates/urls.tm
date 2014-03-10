from django.conf.urls import patterns, include, url
from django.contrib import admin
from settings import MEDIA_ROOT

from django_conventions import UrlsManager
import {app_name}.views as {app_name}_root

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {{'document_root': MEDIA_ROOT, 'show_indexes': True}}),

)

UrlsManager(urlpatterns, {app_name}_root)