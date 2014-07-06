from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', include('eventslist.urls')),
    url(r'^eventslist/', include('eventslist.urls')),
)
