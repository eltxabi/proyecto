from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'eventslist.views.home_page', name='home'),
)
