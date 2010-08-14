from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'website.views.index', name='index'),
    url(r'^profile/$', 'website.profile.views.profile', name='profile'),
    url(r'^', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^adventure/list/$', "website.adventure.views.adventure_list", name="adventure-list"),
    url(r'^adventure/detail/(?P<object_id>\d+)/$', "website.adventure.views.adventure_detail", name="adventure-detail"),
    url(r'^adventure/start/(?P<object_id>\d+)/$', "website.adventure.views.adventure_start", name="adventure-start"),
    url(r'^adventure/location/(?P<adventure_id>\d+)/(?P<location_id>\d+)/$',
        "website.adventure.views.adventure_location",
        name="adventure-location")
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^', include('staticfiles.urls')),
    )
