from django.conf.urls import patterns, include, url
from eventslist import views

urlpatterns = patterns('',
    url(r'^register$', views.register, name='register'),
    url(r'^$', views.home, name='home'),
)

 
