from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', include('core_manager.urls')),
    url(r'^android_api/', include('apis.android_api.urls')),
    url(r'^api/ecb/', include('apis.ecb_bank_collect.urls')),
    url(r'^chama/', include('chama.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
