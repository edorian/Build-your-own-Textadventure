from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'website.views.index', name='index'),
    url(r'^profile/$', 'website.profile.views.profile', name='profile'),
    url(r'^', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^adventure/list/$', "website.adventure.views.player.adventure_list", name="adventure-list"),
    url(r'^adventure/list/my/$',
        'website.adventure.views.player.adventure_list_my',
        name="adventure-list-my"),
    url(r'^adventure/list/by/(?P<username>[^/]+)/$',
        'website.adventure.views.player.adventure_list_by_author',
        name="adventure-list-author"),
    url(r'^adventure/list/language/(?P<language>[^/]+)/$',
        'website.adventure.views.player.adventure_list_by_language',
        name="adventure-list-language"),
    url(r'^adventure/detail/(?P<object_id>\d+)/$',
        'website.adventure.views.player.adventure_detail',
        name="adventure-detail"),
    url(r'^adventure/start/(?P<object_id>\d+)/$',
        'website.adventure.views.player.adventure_start',
        name="adventure-start"),
    url(r'^adventure/location/(?P<adventure_id>\d+)/(?P<location_number>\d+)/$',
        "website.adventure.views.player.adventure_location",
        name="adventure-location"),
    url(r'^adventure/rate/(?P<adventure_id>\d+)/$',
        "website.adventure.views.player.adventure_rating",
        name="adventure-rating"),

    # editor
    url(r'^adventure/create/$',
        'website.adventure.views.editor.adventure_create',
        name='adventure-create'),
    url(r'^adventure/(?P<object_id>\d+)/edit/$',
        'website.adventure.views.editor.adventure_edit',
        name='adventure-edit'),
    url(r'^adventure/(?P<adventure_id>\d+)/delete/$',
        'website.adventure.views.editor.adventure_delete',
        name='adventure-delete'),
    url(r'^adventure/(?P<adventure_id>\d+)/location/create/$',
        'website.adventure.views.editor.location_create',
        name='location-create'),
    url(r'^adventure/(?P<adventure_id>\d+)/location/(?P<location_id>\d+)/edit/$',
        'website.adventure.views.editor.location_edit',
        name='location-edit'),
    url(r'^adventure/(?P<adventure_id>\d+)/location/(?P<location_id>\d+)/delete/$',
        'website.adventure.views.editor.location_delete',
        name='location-delete'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^', include('staticfiles.urls')),
    )
