from django.conf.urls.defaults import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'website.views.index', name='index'),
    url(r'^profile/$', 'website.profile.views.profile', name='profile'),
    url(r'^', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
