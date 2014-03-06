from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst
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

'''
class AuthenticationForm(forms.Form):
    """
Base class for authenticating users. Extend this to get a form that accepts username/password logins.
"""
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': "Please enter a correct %(username)s and password. "
        "Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }

    def __init__(self, request=None, *args, **kwargs):
        """
The 'request' parameter is set for custom auth use by subclasses.
The form data comes in via the standard 'data' kwarg.
"""
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
Controls whether the given User may log in. This is a policy setting,
independent of end-user authentication. This default behavior is to
allow login by active users, and reject login by inactive users.

If the given user cannot log in, this method should raise a
``forms.ValidationError``.

If the given user may log in, this method should return None.
"""
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
'''






