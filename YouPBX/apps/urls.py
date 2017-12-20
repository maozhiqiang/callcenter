import django 
from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
import xadmin
xadmin.ROOT_PATH_NAME = 'xadmin'
settings.XADMIN_EXCLUDE_PLUGINS = ['bookmark']
xadmin.DEFAULT_RELFIELD_STYLE = {'fk': 'fk_select', 'm2m': 'm2m_select2'}
xadmin.autodiscover()

# from xadmin.plugins import xversion
# xversion.register_models()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r'^uploads/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), 
)
