from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst
from django.forms.widgets import Input
from mongoengine.django.auth import User
from eventslist.models import Category

class RangeInput(Input):
    input_type='range'

class SearchForm(forms.Form):
    error_messages = {
        'location_not_selected': "You must select a location",  
	'distance_out_of_range': "Distance must be between 1 and 100",      
    }    

  
    title = forms.CharField(label="Title", max_length=30, required=False)
    category = forms.ChoiceField(label="Category", required=False, widget=forms.Select)
    lat = forms.CharField(required=False,widget=forms.HiddenInput)  
    lng = forms.CharField(required=False,widget=forms.HiddenInput) 
    distance = forms.CharField(label="Distance",widget=RangeInput(attrs={'min':'1','max':'100','value':'1'}))    
 
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        choices = [(unicode(pt), unicode(pt)) for pt in Category.objects.all()]
        self.fields['category'].choices = choices
	self.fields['category'].choices.insert(0,('','Select category'))       
    
    def clean(self):
       cleaned_data = super(SearchForm,self).clean()
       lat = cleaned_data.get("lat")
       lng = cleaned_data.get("lng")
       distance = cleaned_data.get("distance")
       
       if not lat or not lng:
          raise forms.ValidationError(self.error_messages['location_not_selected']) 
       
       if (int(distance)<1) or (int(distance)>100):
	  raise forms.ValidationError(self.error_messages['distance_out_of_range']) 

       return cleaned_data 

class RegistrationForm(forms.Form):
    error_messages = {
        'duplicate_username': "A user with that username already exists.",
        'password_mismatch': "The two password fields didn't match.",
    }
    username = forms.RegexField(label="Username", max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text="Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only.",
        error_messages={
            'invalid': "This value may contain only letters, numbers and "
                         "@/./+/-/_ characters."})
    password1 = forms.CharField(label="Password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.")

    def clean(self):
       cleaned_data = super(RegistrationForm,self).clean()
       user_name = cleaned_data.get("username")
       password1 = cleaned_data.get("password1")
       password2 = cleaned_data.get("password2")
       if password1!=password2:
          raise forms.ValidationError(self.error_messages['password_mismatch']) 
       
       if User.objects(username=user_name).count()==1:
	  raise forms.ValidationError(self.error_messages['duplicate_username'])     

       return cleaned_data	


class CommentForm(forms.Form):
    content = forms.CharField(label="Comment",widget=forms.Textarea)
    
class EventForm(forms.Form):
    error_messages = {
        'location_not_selected': "You must select a location",       
    }    

    title = forms.CharField(label="Title", max_length=30)
    description = forms.CharField(label="Description",widget=forms.Textarea)
    category = forms.ChoiceField(label="Category",widget=forms.Select)
    photo = forms.ImageField(required=False)	
    lat = forms.CharField(required=False,widget=forms.HiddenInput)  
    lng = forms.CharField(required=False,widget=forms.HiddenInput) 

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        choices = [(unicode(pt), unicode(pt)) for pt in Category.objects.all()]
        self.fields['category'].choices = choices
	self.fields['category'].choices.insert(0,('','Select category'))       
    
    def clean(self):
       cleaned_data = super(EventForm,self).clean()
       lat = cleaned_data.get("lat")
       lng = cleaned_data.get("lng")
       
       if not lat or not lng:
          raise forms.ValidationError(self.error_messages['location_not_selected']) 
       
       return cleaned_data  








