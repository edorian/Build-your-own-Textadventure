from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'website.views.index', name='index'),
    url(r'^profile/$', 'website.profile.views.profile', name='profile'),
    url(r'^', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^', include('staticfiles.urls')),
    )
