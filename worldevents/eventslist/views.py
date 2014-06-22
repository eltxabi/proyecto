
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

def home(request,num_events='15'):
   '''
   if hasattr(request,'session'):
	   if "search_query" in request.session:
	   	messages.success(request,request.session["search_query"])
   '''
   if "event_list" not in request.session:
   	if "search_query" in request.session:
		event_list=Event.search(request.session['search_query']['title'],request.session['search_query']['category'],request.session['search_query']['lat'],request.session['search_query']['lng'],request.session['search_query']['distance'],int(num_events))
   	else:
   		event_list = Event.objects.order_by('-added_date')[int(num_events)-15:int(num_events)]
   else:
	event_list=request.session['event_list'] 
	del request.session['event_list']  

   form = CommentForm()
   return render(request, "eventslist/home.html", {'event_list':event_list,'num_events':num_events,'form':form,})  

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

def searchevents(request):
   if request.method == 'POST':
	form = SearchForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
	    category=form.cleaned_data['category'] 
	    lat=form.cleaned_data['lat']
	    lng=form.cleaned_data['lng'] 
	    distance=form.cleaned_data['distance']
	    
	    event_list=Event.search(title,category,lat,lng,distance,15)
	    
	    if event_list:
			
		request.session["search_query"]={'title':title,'category':category,'lat':lat,'lng':lng,'distance':distance,'num_events':15}
		request.session["event_list"]=list(event_list)
		
	    else:
		messages.success(request,'No search results')
	    
	    return HttpResponseRedirect("/")
   else:
	form = SearchForm()
   return render(request, "eventslist/searchevents.html", {'form':form,})     
  
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
	if form.is_valid():
	    User.create_user(form.cleaned_data['username'],form.cleaned_data['password1'])  
	    messages.success(request, form.cleaned_data['username'] + ' you have been successfully registered')
	    print 'valido'
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

@login_required
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
	if event.photo is not None:
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
        'form': form, 'photo': Event.objects(id=event_id)[0].photo, 'id': event_id,
    }) 

