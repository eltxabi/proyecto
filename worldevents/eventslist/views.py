
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

def home(request):
   if hasattr(request,'session'):
	   for s in request.session.iteritems():
		messages.success(request,s) 
   
   event_list = Event.objects.order_by('added_date')
   form = CommentForm()
   return render(request, "eventslist/home.html", {'event_list':event_list,'form':form,})  

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
	    event_list=Event.objects(Q(title__icontains=title) & Q(category=category) & Q(location__geo_within_sphere=[(float(lat),float(lng)),float(distance)]))
	    form=SearchForm()
	    return render(request, "eventslist/home.html", {'event_list':event_list,})  
   else:
	form = SearchForm()
   return render(request, "eventslist/searchevents.html", {'form':form,})     
  
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
	    event = Event(title=title,description=description,category=category)		
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

