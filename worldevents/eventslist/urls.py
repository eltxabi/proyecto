from django.conf.urls import patterns, include, url
from eventslist import views

urlpatterns = patterns('',
    url(r'^deleteevent/(\w+)$', views.deleteevent, name='deleteevent'),
    url(r'^deleteevent$', views.deleteevent, name='deleteevent'),
    url(r'^editevent/(\w+)$', views.editevent, name='editevent'),
    url(r'^editevent$', views.editevent, name='editevent'),
    url(r'^searchevents/(\d+)/$', views.searchevents, name='searchevents'),
    url(r'^searchevents/(\d+)$', views.searchevents, name='searchevents'),
    url(r'^searchevents$', views.searchevents, name='searchevents'),	
    url(r'^addevent$', views.addevent, name='addevent'),
    url(r'^addcomment$', views.addcomment, name='addcomment'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.loginpage, name='login'),
    url(r'^logout$', views.logoutpage, name='logout'),	
    url(r'^$', views.home, name='home'),
)

 
