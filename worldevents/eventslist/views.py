
from eventslist.forms import RegistrationForm,EventForm
from eventslist.models import Category,Event
from django.http import HttpResponseRedirect
from django.shortcuts import render
from mongoengine.django.auth import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
import mongoengine

def home(request):
   if hasattr(request,'session'):
	   for s in request.session.iteritems():
		messages.success(request,s) 
   return render(request,'eventslist/home.html')

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

def addevent(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
	    description=form.cleaned_data['description']
            category=form.cleaned_data['category'] 
            event = Event(title=title,description=description,category=category) 
            event.save() 	
            messages.success(request, title + ' has been created')
            return HttpResponseRedirect("/")
    else:
        form = EventForm()
       
    return render(request,'eventslist/addevent.html', {
        'form': form,
    })  

