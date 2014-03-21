from django.conf.urls import patterns, include, url
from eventslist import views

urlpatterns = patterns('',
    url(r'^searchevents$', views.searchevents, name='searchevents'),	
    url(r'^addevent$', views.addevent, name='addevent'),
    url(r'^addcomment$', views.addcomment, name='addcomment'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.loginpage, name='login'),
    url(r'^logout$', views.logoutpage, name='logout'),	
    url(r'^$', views.home, name='home'),
)

 
