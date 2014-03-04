
from eventslist.forms import RegistrationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from mongoengine.django.auth import User
from django.contrib import messages

def home(request):
   return render(request,'eventslist/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
	    new_user = User(form.cleaned_data['username'],form.cleaned_data['password1'])
	    new_user.save()
	    messages.success(request, 'You have been successfully registered')
            return HttpResponseRedirect("/")
    else:
        form = RegistrationForm()
    return render(request, "eventslist/register.html", {
        'form': form,
    })  
  
