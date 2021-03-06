
from eventslist.forms import RegistrationForm,EventForm,SearchForm,CommentForm
from eventslist.models import Category,Event,Comment
from django.http import HttpResponseRedirect
from django.shortcuts import render
from mongoengine.queryset import Q
from mongoengine.django.auth import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from mongoengine import *
from django.conf import settings
from time import time
import os
import urllib

def home(request):
   
   '''
   if hasattr(request,'session'):
	   for s in request.session.iteritems():
		messages.success(request,s)
   '''

   events_list = Event.objects.order_by('-added_date')[0:20]
   form = CommentForm()
   return render(request, "eventslist/home.html", {'events_list':events_list,'num_events':'20','form':form,})  

@login_required
def addcomment(request):
   if request.method == 'POST':
	event_id=request.POST['event_id']
	form = CommentForm(request.POST)
	if form.is_valid():
	    content=form.cleaned_data['content']
	    user=request.user.username
	    comment=Comment(content=content,user=user)
            Event.objects(id=event_id).update_one(push__comments=comment)
	    form = CommentForm()
   else:
	form = CommentForm()

   event=Event.objects.get(id=event_id) 
   return render(request, "eventslist/comments.html", {'form':form,'event':event}) 

def searchevents(request,num_events=0):
   if request.method == 'POST':
	form = SearchForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
	    category=form.cleaned_data['category'] 
	    lat=form.cleaned_data['lat']
	    lng=form.cleaned_data['lng'] 
	    distance=form.cleaned_data['distance']
	    
	    events_list=Event.search(title,category,lat,lng,distance,20)
	    
	    if events_list:
		search_query=urllib.urlencode( {'title':title,'category':category,'lat':lat,'lng':lng,'distance':distance,'num_events':20} )
	    else:
		messages.success(request,'No search results')
	    
	    return render(request, "eventslist/eventslist.html", {'events_list':events_list,'search_query':search_query,'num_events':20}) 
	else:
	    print("formulario invalido")
	    return render(request, "eventslist/searchevents.html", {'form':form,})  
   elif(num_events==0):
	form = SearchForm()
   	return render(request, "eventslist/searchevents.html", {'form':form,})     
   elif request.META['QUERY_STRING']:
	title=request.GET['title']
        category=request.GET['category'] 
	lat=request.GET['lat']
	lng=request.GET['lng'] 
	distance=request.GET['distance']
	events_list=Event.search(title,category,lat,lng,distance,int(num_events))
	
	if events_list:
		search_query=urllib.urlencode( {'title':title,'category':category,'lat':lat,'lng':lng,'distance':distance,'num_events':20} )
	else:
		messages.success(request,'No search results')
	    
	return render(request, "eventslist/eventslist.html", {'events_list':events_list,'search_query':search_query,'num_events':num_events}) 
	
   else:
	events_list = Event.objects.order_by('-added_date')[int(num_events)-20:int(num_events)]
	return render(request, "eventslist/eventslist.html", {'events_list':events_list,'num_events':num_events}) 
  
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.create_user(form.cleaned_data['username'],form.cleaned_data['password1'])  
	    messages.success(request, form.cleaned_data['username'] + ' you have been successfully registered')
            return HttpResponseRedirect("/")	
    else:
        form = RegistrationForm()
    return render(request, "eventslist/register.html", {
        'form': form,
    })  

def loginpage(request):
   if request.method == 'POST':
        form = AuthenticationForm(request.POST)
	username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
	if user is not None:
	   login(request,user)
	   messages.success(request,'Login correcto ' + user.username)
	   return HttpResponseRedirect("/")
        else:
           messages.success(request,'Login incorrecto')    
   else:
        form = AuthenticationForm()
   
   if hasattr(request,'session'):
	   for s in request.session.iteritems():
		messages.success(request,s) 
	   
   return render(request,'eventslist/login.html', {
        'form': form,
    })  

def logoutpage(request):
   logout(request)
   return HttpResponseRedirect("/")

@login_required
def addevent(request):
    if request.method == 'POST':
	form = EventForm(request.POST, request.FILES)
	
	if form.is_valid():
            title=form.cleaned_data['title']
	    description=form.cleaned_data['description']
            category=form.cleaned_data['category'] 
	    lat=form.cleaned_data['lat']
	    lng=form.cleaned_data['lng']
	    user=request.user.username
	    event = Event(title=title,description=description,category=category,user=user)		
	    if (request.FILES):
		photo_name=request.user.username+"-"+str(int(time()))+".jpeg"
		f=request.FILES["photo"]
		with open(settings.MEDIA_ROOT+photo_name, 'wb+') as destination:
        		for chunk in f.chunks():
            			destination.write(chunk)
	    	event.photo=photo_name
            event.location=[float(lat),float(lng)] 
            event.save() 	
            messages.success(request, title + ' has been created')
            return HttpResponseRedirect("/")
    else:
	form = EventForm()
      
    return render(request,'eventslist/addevent.html', {
        'form': form,
    })  


@login_required
def deleteevent(request,event_id):
    if request.method == 'POST':
	event=Event.objects(id=event_id)[0]
	os.remove(settings.MEDIA_ROOT+event.photo)
	event.delete()
	return HttpResponseRedirect("/")
    
    return render(request,'eventslist/deleteevent.html', {
        'id': event_id,
    }) 

@login_required
def editevent(request,event_id):
    if request.method == 'POST':
	form = EventForm(request.POST, request.FILES)
	
	if form.is_valid():
            title=form.cleaned_data['title']
	    description=form.cleaned_data['description']
            category=form.cleaned_data['category'] 
	    photo=Event.objects(id=event_id)[0].photo
	    lat=form.cleaned_data['lat']
	    lng=form.cleaned_data['lng']
	    user=request.user.username
	    event = Event(id=event_id,title=title,description=description,category=category,photo=photo,user=user)		
	    if (request.FILES):
		if photo is not None:
			os.remove(settings.MEDIA_ROOT+photo)	
		photo_name=request.user.username+"-"+str(int(time()))+".jpeg"
		f=request.FILES["photo"]
		with open(settings.MEDIA_ROOT+photo_name, 'wb+') as destination:
        		for chunk in f.chunks():
            			destination.write(chunk)
	    	event.photo=photo_name
            event.location=[float(lat),float(lng)] 
            event.save() 	
            messages.success(request, title + ' has been updated')
            return HttpResponseRedirect("/")
    else:
	form = EventForm()
	event=Event.objects(id=event_id)[0]
	form.fields["title"].initial = event.title
	form.fields["description"].initial = event.description
	form.fields["category"].initial = event.category
	form.fields["lat"].initial = event.location['coordinates'][0]
	form.fields["lng"].initial = event.location['coordinates'][1]
	      
    return render(request,'eventslist/editevent.html', {
        'form': form, 'photo': event.photo, 'id': event_id,
    }) 

