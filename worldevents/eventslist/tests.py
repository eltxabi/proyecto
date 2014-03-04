from django.test.simple import DjangoTestSuiteRunner
from django.test import LiveServerTestCase
from django.core.urlresolvers import resolve
from eventslist.views import home,register
from django.http import HttpRequest
from django.template.loader import render_to_string
from eventslist.forms import RegistrationForm
from django.utils.html import escape
from mongoengine.django.auth import User

from eventslist.models import Entrada

class HomeTest(LiveServerTestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        pass

    def test_root_resolves_home_view(self):
	page=resolve('/')
	self.assertEqual(page.func, home)

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'eventslist/home.html')

    def test_home_page_returns_correct_html(self):
        request = HttpRequest() 
        response = home(request)  
        expected_html = render_to_string('eventslist/home.html')
        self.assertEqual(response.content.decode(), expected_html)



class RegisterTest(LiveServerTestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        pass

    def test_register_link_resolves_register_view(self):
	page=resolve('/eventslist/register')
	self.assertEqual(page.func, register)

    def test_register_page_returns_correct_html(self):
        request = HttpRequest() 
        response = register(request)  
        expected_html = render_to_string('eventslist/register.html',{
        'form': RegistrationForm()})
        self.assertEqual(response.content.decode(), expected_html)

    def test_register_page_uses_item_form(self):
        response = self.client.get('/eventslist/register')
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_register_page_save_user_to_database(self):
	response = self.client.post('/eventslist/register',data={'username': 'john','password1': 'john','password2': 'john'}) 
	self.assertEqual(User.objects(username='john').count(),1) 

    def test_register_page_send_success_message_to_home(self):
	response = self.client.post('/eventslist/register',data={'username': 'john','password1': 'john','password2': 'john'}) 
	expected_html='You have been successfully registered'
        self.assertIn(expected_html,response.content)
	
	
class RegistrationFormTest(LiveServerTestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        pass

 
    def test_validation_errors_are_sent_back_to_register_template(self):
        response = self.client.post('/eventslist/register')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventslist/register.html')
        expected_error = escape("This field is required.")
        self.assertContains(response, expected_error)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/eventslist/register',data={'username': '$'})
        self.assertIsInstance(response.context['form'], RegistrationForm)
	expected_input = escape('<input id="id_username" maxlength="30" name="username" type="text" value="$" />')
        self.assertIn(expected_input,escape(response.content)) 


    def test_form_validation_for_blank_items(self):
        form = RegistrationForm(data={'username': '','password1': '','password2': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'],["This field is required."])
        self.assertEqual(form.errors['password1'],["This field is required."])
        self.assertEqual(form.errors['password2'],["This field is required."])

    
    def test_form_validation_for_different_passwords(self):
	form = RegistrationForm(data={'username': 'John','password1': 'a','password2': 'b'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(),["The two password fields didn't match."])


       
    def test_form_validation_for_duplicate_username(self):
        response = self.client.post('/eventslist/register',data={'username': 'john','password1': 'john','password2': 'john'})
	response = self.client.post('/eventslist/register',data={'username': 'john','password1': 'john','password2': 'john'})
	expected_input = escape('A user with that username already exists.')
        self.assertIn(expected_input,escape(response.content))








'''
class NoSQLTestCase(TestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        pass

    def test_bad_maths(self):
	entrada = Entrada(title='probandol')
	entrada.save()
	for e in Entrada.objects:
	   self.assertEqual(e.title,'probandolo')
	
        self.assertEqual(1 + 1, 3)

'''






