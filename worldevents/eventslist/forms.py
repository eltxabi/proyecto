from django import forms
from mongoengine.django.auth import User

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









