from django.test import LiveServerTestCase,Client
from django.core.urlresolvers import resolve
from eventslist.views import home,register,loginpage,logoutpage,addevent,searchevents,editevent,deleteevent,addcomment
from eventslist.models import Event,Category
from django.http import HttpRequest
from django.template.loader import render_to_string
from eventslist.forms import RegistrationForm,EventForm,SearchForm,CommentForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.utils.html import escape
from mongoengine.django.auth import User
from pymongo import Connection
import unittest
from auth import PasswordUtils
import os
from django.conf import settings

class HomeTest(LiveServerTestCase):
    def _fixture_setup(self):
        c=Category(name='Musica')
        c.save()
	c=Category(name='Restauracion')
        c.save()
	user=User.create_user('john','john')
	request = HttpRequest() 
	user=User.objects(username='john')
	self.client.login(username='john',password='john')
           
    def _fixture_teardown(self):
        Category.objects.all().delete()
        Event.objects.all().delete()
	self.client.logout()
        User.objects(username='john').delete()  
    
        
    def test_root_resolves_home_view(self):
	page=resolve('/')
	self.assertEqual(page.func, home)

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'eventslist/home.html')

    def test_home_page_show_events_list(self):
        response = self.client.get('/')
	num_events = response.content.count('</tr>')
	self.assertEqual(Event.objects().count(),num_events) 


    def test_home_page_show_events_pages(self):
	for i in range(45):
		response = self.client.post('/eventslist/addevent',data={'title': 'Concierto'+str(i),'description': 'Es un concierto','category': 'Musica','lat':'49.8','lng':'4.7'})
	response = self.client.get('/')
	num_events = response.content.count('</tr>')
	self.assertEqual(num_events,15)
	expected_input = escape('<td>Concierto44</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<td>Concierto30</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<a href="/eventslist/30">')
	self.assertIn(expected_input,escape(response.content))
	response = self.client.get('/eventslist/30')
	num_events = response.content.count('</tr>')
	self.assertEqual(num_events,15)
	expected_input = escape('<td>Concierto29</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<td>Concierto15</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<a href="/eventslist/45">')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<a href="/eventslist/15">')
	self.assertIn(expected_input,escape(response.content))
	response = self.client.get('/eventslist/15')
	num_events = response.content.count('</tr>')
	self.assertEqual(num_events,15)
	expected_input = escape('<td>Concierto44</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<td>Concierto30</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<a href="/eventslist/30">')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<a href="/eventslist/30">')
	self.assertIn(expected_input,escape(response.content))

        
	
    def test_events_details_are_in_home_page(self):
	response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category': 'Musica','lat':'49.8','lng':'4.7'}) 
	response = self.client.post('/eventslist/addevent',data={'title': 'Concierto2','description': 'Es un concierto2','category': 'Musica','lat':'49.8','lng':'4.7'}) 
	self.assertEqual(Event.objects(title='Concierto').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto')),'[<Event: Concierto-49.84.7-Es un concierto-Musica>]')
	self.assertEqual(Event.objects(title='Concierto2').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto2')),'[<Event: Concierto2-49.84.7-Es un concierto2-Musica>]')
	self.assertEqual(Event.objects().count(),2) 
	response = self.client.get('/')
	expected_input = escape('<td>Concierto</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<td>Concierto2</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<li>Concierto</li>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<li>Concierto2</li>')
	self.assertIn(expected_input,escape(response.content))

    def test_events_photos_are_in_home_page(self):
	myphoto = open('static/media/prueba.jpeg','r') 
        response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category': 'Musica','lat':'49.8','lng':'4.7','photo':myphoto}) 
	self.assertEqual(Event.objects(title='Concierto').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto')),'[<Event: Concierto-49.84.7-Es un concierto-Musica>]')
	response = self.client.get('/')
	expected_input = escape(Event.objects(title='Concierto')[0].photo)
	self.assertIn(expected_input,escape(response.content))
	os.remove(settings.MEDIA_ROOT+str(Event.objects(title='Concierto')[0].photo))
	



class RegisterTest(LiveServerTestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        User.objects(username='john').delete() 
	User.objects(username='bob').delete()

    def test_register_link_resolves_register_view(self):
	page=resolve('/eventslist/register')
	self.assertEqual(page.func, register)

    def test_register_page_returns_correct_html(self):
        request = HttpRequest() 
        response = register(request)  
        expected_html = render_to_string('eventslist/register.html',{'form': RegistrationForm()})
        self.assertEqual(response.content.decode(), expected_html)

    def test_register_page_uses_registration_form(self):
        response = self.client.get('/eventslist/register')
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_register_page_save_user_to_database(self):
	response = self.client.post('/eventslist/register',data={'username': 'john','password1': 'john','password2': 'john'}) 
	self.assertEqual(User.objects(username='john').count(),1) 

    def test_register_page_send_success_message_to_home(self):
	response = self.client.post('/eventslist/register',data={'username': 'bob','password1': 'bob','password2': 'bob'},follow=True) 
	expected_html='you have been successfully registered'
        self.assertIn(expected_html,response.content)
	
class RegistrationFormTest(LiveServerTestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        User.objects(username='john').delete() 

 
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
	

class LoginTest(LiveServerTestCase):
    def _fixture_setup(self):
        user=User.create_user('john','john')
    def _fixture_teardown(self):
        User.objects(username='john').delete()  

    def test_login_link_resolves_login_view(self):
	page=resolve('/eventslist/login')
	self.assertEqual(page.func, loginpage)

    def test_login_page_returns_correct_html(self):
        request = HttpRequest() 
        response = loginpage(request)  
        expected_html = render_to_string('eventslist/login.html',{
        'form': AuthenticationForm()})
        self.assertEqual(response.content.decode(), expected_html)

    def test_login_page_uses_authentication_form(self):
        response = self.client.get('/eventslist/login')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_login_page_login_user(self):
	response = self.client.post('/eventslist/login',data={'username': 'john','password': 'john'}) 
	self.assertIn(response.content.decode(),'john')


class LoginFormTest(LiveServerTestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
	pass
        
    def test_form_validation_for_blank_items(self):
	response = self.client.post('/eventslist/login',data={'username': '','password': ''})
        expected_input = escape('Login incorrecto')
	self.assertIn(expected_input,escape(response.content))

    def test_form_validation_for_blank_username(self):
	response = self.client.post('/eventslist/login',data={'username': '','password': '111'})
        expected_input = escape('Login incorrecto')
	self.assertIn(expected_input,escape(response.content))

    def test_form_validation_for_blank_password(self):
	response = self.client.post('/eventslist/login',data={'username': '111','password': ''})
        expected_input = escape('Login incorrecto')
	self.assertIn(expected_input,escape(response.content))
          
    def test_form_validation_for_wrong_data(self):
	response = self.client.post('/eventslist/login',data={'username': '111','password': '111'})
        expected_input = escape('Login incorrecto')
	self.assertIn(expected_input,escape(response.content))
    

class LogoutTest(LiveServerTestCase):
    def _fixture_setup(self):
        User.create_user('john','john')
	user=User.objects(username='john')
	self.client.login(username='john',password='john')

    def _fixture_teardown(self):
        User.objects(username='john').delete()

    def test_logout_link_resolves_logout_view(self):
	page=resolve('/eventslist/logout')
	self.assertEqual(page.func, logoutpage)

    def test_user_can_logout(self):
	self.client.logout()
	response = self.client.get('/')
	expected_input = escape('Login')
	self.assertIn(expected_input,escape(response.content))
	
	
class AddEventTest(LiveServerTestCase):
    def _fixture_setup(self):
        c=Category(name='Musica')
        c.save()
	c=Category(name='Restauracion')
        c.save()
        user=User.create_user('john','john')
	request = HttpRequest() 
	user=User.objects(username='john')
	self.client.login(username='john',password='john')
         
        
    def _fixture_teardown(self):
        Category.objects.all().delete()
        Event.objects.all().delete()
	self.client.logout()
        User.objects(username='john').delete()  
    
    def test_addevent_page_requires_login_user(self):
	self.client.logout()
	response = self.client.get('/eventslist/addevent',follow=True)
	self.assertEqual(response.status_code,200)
	self.assertRedirects(response,'/eventslist/login?next=/eventslist/addevent')
    
    def test_addevent_link_resolves_addevent_view(self):
	page=resolve('/eventslist/addevent')
	self.assertEqual(page.func, addevent)
    
    def test_addevent_page_uses_addevent_form(self):
	response = self.client.get('/eventslist/addevent')
	self.assertIsInstance(response.context['form'], EventForm)

    def test_addevent_page_save_event_to_database_and_create_photo_file(self):
	myphoto = open('static/media/prueba.jpeg','r') 
        response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category': 'Musica','lat':'49.8','lng':'4.7','photo':myphoto}) 
	self.assertEqual(Event.objects(title='Concierto').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto')),'[<Event: Concierto-49.84.7-Es un concierto-Musica>]')
	self.assertTrue(str(Event.objects(title='Concierto')[0].photo).find('john')==0)
	self.assertTrue(os.path.isfile(settings.MEDIA_ROOT+str(Event.objects(title='Concierto')[0].photo)))
	os.remove(settings.MEDIA_ROOT+str(Event.objects(title='Concierto')[0].photo))
	

    def test_addevent_page_send_success_message_to_home(self):
	response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category':'Musica','lat':'49.8','lng':'4.7'},follow=True)  
	expected_html='has been created'
	self.assertIn(expected_html,response.content)
	
 


class EventFormTest(LiveServerTestCase):
    def _fixture_setup(self):
        c=Category(name='Musica')
        c.save()
	c=Category(name='Restauracion')
        c.save()
	user=User.create_user('john','john')
	request = HttpRequest() 
	user=User.objects(username='john')
	self.client.login(username='john',password='john')
 
    def _fixture_teardown(self):
        Category.objects.all().delete()
        Event.objects.all().delete()
	self.client.logout()
        User.objects(username='john').delete()  
        
    def test_event_form_load_categories_from_db(self):
        response = self.client.get('/eventslist/addevent')
        for c in Category.objects().all() :   
            self.assertIn('<option value="'+c.name+'">'+c.name+'</option>',response.content.decode())        

    def test_validation_errors_are_sent_back_to_addevent_template(self):
        response = self.client.post('/eventslist/addevent')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventslist/addevent.html')
        expected_error = escape("This field is required.")
        self.assertContains(response, expected_error)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/eventslist/addevent',data={'title': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'})
	self.assertIsInstance(response.context['form'], EventForm)
	expected_input = escape('<input id="id_title" maxlength="30" name="title" type="text" value="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" />')
        self.assertIn(expected_input,escape(response.content)) 

    def test_form_validation_for_blank_items(self):
	response = self.client.post('/eventslist/addevent',data={'title': '','description': '','category':'','lat':'','lng':''})
        expected_input = escape('This field is required.')
	self.assertIn(expected_input,escape(response.content))

    def test_form_validation_for_blank_location(self):
	response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category':'Musica','lat':'','lng':''}) 
        expected_input = escape('You must select a location')
	self.assertIn(expected_input,escape(response.content))



class EditEventTest(LiveServerTestCase):
    def _fixture_setup(self):
        c=Category(name='Musica')
        c.save()
	c=Category(name='Restauracion')
        c.save()
        user=User.create_user('john','john')
	request = HttpRequest() 
	user=User.objects(username='john')
	self.client.login(username='john',password='john')
         
        
    def _fixture_teardown(self):
        Category.objects.all().delete()
        Event.objects.all().delete()
	self.client.logout()
        User.objects(username='john').delete()  
    
    def test_editevent_page_requires_login_user(self):
	self.client.logout()
	response = self.client.get('/eventslist/editevent',follow=True)
	self.assertEqual(response.status_code,200)
	self.assertRedirects(response,'/eventslist/login?next=/eventslist/editevent')
    
    def test_editevent_link_resolves_editevent_view(self):
	page=resolve('/eventslist/editevent')
	self.assertEqual(page.func, editevent)

    def test_editevent_page_uses_editevent_form(self):
	response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category':'Musica','lat':'49.8','lng':'4.7'}) 
        self.assertEqual(Event.objects(title='Concierto').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto')),'[<Event: Concierto-49.84.7-Es un concierto-Musica>]')
	event_id=Event.objects(title='Concierto')
	response = self.client.get('/eventslist/editevent/'+str(event_id[0].id))
	self.assertIsInstance(response.context['form'], EventForm)

    def test_editevent_page_save_event_to_database_save_photo_file(self):
	response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category':'Musica','lat':'49.8','lng':'4.7'}) 
        self.assertEqual(Event.objects(title='Concierto').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto')),'[<Event: Concierto-49.84.7-Es un concierto-Musica>]')
	event_id=Event.objects(title='Concierto')
	event_id_old=event_id[0].id
	myphoto = open('static/media/prueba.jpeg','r')
	response = self.client.post('/eventslist/editevent/'+str(event_id[0].id),data={'title': 'ConciertoModificado','description': 'Es un concierto Modificado','category':'Musica','lat':'49.8','lng':'4.7','photo':myphoto},follow=True) 
	self.assertEqual(Event.objects(title='Concierto').count(),0)
	self.assertEqual(Event.objects(title='ConciertoModificado').count(),1)
	self.assertEqual(str(Event.objects(title='ConciertoModificado')),'[<Event: ConciertoModificado-49.84.7-Es un concierto Modificado-Musica>]')
	event_id_modificado=Event.objects(title='ConciertoModificado')
	self.assertEqual(event_id_old,event_id_modificado[0].id)
	self.assertTrue(str(Event.objects(title='ConciertoModificado')[0].photo).find('john')!=-1)
	self.assertTrue(os.path.isfile(settings.MEDIA_ROOT+str(Event.objects(title='ConciertoModificado')[0].photo)))
	os.remove(settings.MEDIA_ROOT+str(Event.objects(title='ConciertoModificado')[0].photo))
	

    def test_editevent_page_send_success_message_to_home(self):
	response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category':'Musica','lat':'49.8','lng':'4.7'},follow=True) 
	event_id=Event.objects(title='Concierto')
	response = self.client.post('/eventslist/editevent/'+str(event_id[0].id),data={'title': 'ConciertoModificado','description': 'Es un concierto Modificado','category':'Musica','lat':'49.8','lng':'4.7'},follow=True) 
	expected_html='has been updated'
	self.assertIn(expected_html,response.content)
    

class EditEventFormTest(LiveServerTestCase):
    def _fixture_setup(self):
        c=Category(name='Musica')
        c.save()
	c=Category(name='Restauracion')
        c.save()
	user=User.create_user('john','john')
	request = HttpRequest() 
	user=User.objects(username='john')
	self.client.login(username='john',password='john')
 
    def _fixture_teardown(self):
        Category.objects.all().delete()
        Event.objects.all().delete()
	self.client.logout()
        User.objects(username='john').delete()  
        
    def test_edit_event_form_load_categories_from_db(self):
	response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category':'Musica','lat':'49.8','lng':'4.7'}) 
        self.assertEqual(Event.objects(title='Concierto').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto')),'[<Event: Concierto-49.84.7-Es un concierto-Musica>]')
	event_id=Event.objects(title='Concierto')
        response = self.client.get('/eventslist/editevent/'+str(event_id[0].id))
        for c in Category.objects().all() :   
            self.assertIn('<option value="'+c.name+'"',response.content.decode())        
    
    def test_validation_errors_are_sent_back_to_editevent_template(self):
        response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category':'Musica','lat':'49.8','lng':'4.7'}) 
        self.assertEqual(Event.objects(title='Concierto').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto')),'[<Event: Concierto-49.84.7-Es un concierto-Musica>]')
	event_id=Event.objects(title='Concierto')
        response = self.client.post('/eventslist/editevent/'+str(event_id[0].id),data={'title': '','description': '','category':'Musica','lat':'49.8','lng':'4.7'},follow=True) 
	self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventslist/editevent.html')
        expected_error = escape("This field is required.")
        self.assertContains(response, expected_error)

    def test_data_are_sent_to_editevent_template(self):
        response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category':'Musica','lat':'49.8','lng':'4.7'}) 
        self.assertEqual(Event.objects(title='Concierto').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto')),'[<Event: Concierto-49.84.7-Es un concierto-Musica>]')
	event_id=Event.objects(title='Concierto')
        event_id_old=event_id[0].id
	response = self.client.get('/eventslist/editevent/'+str(event_id[0].id)) 
	self.assertIn('Concierto',escape(response.content)) 
	self.assertIn('Es un concierto',escape(response.content)) 
	self.assertIn('49.8',escape(response.content)) 
	self.assertIn('4.7',escape(response.content)) 

class DeleteEventTest(LiveServerTestCase):
    def _fixture_setup(self):
        c=Category(name='Musica')
        c.save()
	c=Category(name='Restauracion')
        c.save()
        user=User.create_user('john','john')
	request = HttpRequest() 
	user=User.objects(username='john')
	self.client.login(username='john',password='john')
         
        
    def _fixture_teardown(self):
        Category.objects.all().delete()
        Event.objects.all().delete()
	self.client.logout()
        User.objects(username='john').delete()  
    
    def test_deleteevent_page_requires_login_user(self):
	self.client.logout()
	response = self.client.get('/eventslist/deleteevent',follow=True)
	self.assertEqual(response.status_code,200)
	self.assertRedirects(response,'/eventslist/login?next=/eventslist/deleteevent')
    
    def test_deleteevent_link_resolves_deleteevent_view(self):
	page=resolve('/eventslist/deleteevent')
	self.assertEqual(page.func, deleteevent)

    def test_deleteevent_page_delete_event_from_database_and_photo_file(self):
	myphoto = open('static/media/prueba.jpeg','r') 
        response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category': 'Musica','lat':'49.8','lng':'4.7','photo':myphoto}) 
	self.assertEqual(Event.objects(title='Concierto').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto')),'[<Event: Concierto-49.84.7-Es un concierto-Musica>]')
	event_id=Event.objects(title='Concierto')
	photo_file=event_id[0].photo
	response = self.client.post('/eventslist/deleteevent/'+str(event_id[0].id)) 
	self.assertEqual(Event.objects(title='Concierto').count(),0)
	self.assertFalse(os.path.isfile(settings.MEDIA_ROOT+str(photo_file)))
	



class SearchTest(LiveServerTestCase):
    def _fixture_setup(self):
        c=Category(name='Musica')
        c.save()
	c=Category(name='Restauracion')
        c.save()
                
        
    def _fixture_teardown(self):
        Category.objects.all().delete()
        Event.objects.all().delete()
	self.client.logout()
	User.objects(username='john').delete() 

    def test_searchevents_link_resolves_searchevents_view(self):
	page=resolve('/eventslist/searchevents')
	self.assertEqual(page.func, searchevents)
            
    def test_search_page_uses_search_form(self):
	response = self.client.get('/eventslist/searchevents')
	self.assertIsInstance(response.context['form'], SearchForm)

    def test_search_form_return_correct_events(self):
        user=User.create_user('john','john')
	request = HttpRequest() 
	user=User.objects(username='john')
	self.client.login(username='john',password='john')
	'''AnADIR MAS PRUEBAS DE BUSQUEDA'''
	response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category': 'Musica','lat':'49.8','lng':'4.7'}) 
	self.assertEqual(Event.objects(title='Concierto').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto')),'[<Event: Concierto-49.84.7-Es un concierto-Musica>]')

	response = self.client.post('/eventslist/searchevents',data={'title': 'Concierto','category': 'Musica','lat':'49.8','lng':'4.7','distance':'4'},follow=True) 
	self.assertContains(response,'<li>Concierto</li>')
	self.assertContains(response,'<li>Es un concierto</li>')
	self.assertContains(response,'<li>Musica</li>')
	User.objects(username='john').delete()


    def test_search_show_events_pages(self):
	user=User.create_user('john','john')
	user=User.objects(username='john')
	self.client.login(username='john',password='john')
	for i in range(45):
		response = self.client.post('/eventslist/addevent',data={'title': 'Concierto'+str(i),'description': 'Es un concierto','category': 'Musica','lat':'49.8','lng':'4.7'})
	response = self.client.post('/eventslist/searchevents',data={'lat':'49.8','lng':'4.7','distance':'4'},follow=True)
	num_events = response.content.count('</tr>')
	self.assertEqual(num_events,15)
	expected_input = escape('<td>Concierto44</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<td>Concierto30</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<a href="/eventslist/30">')
	self.assertIn(expected_input,escape(response.content))
	response = self.client.get('/eventslist/30')
	num_events = response.content.count('</tr>')
	self.assertEqual(num_events,15)
	expected_input = escape('<td>Concierto29</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<td>Concierto15</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<a href="/eventslist/45">')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<a href="/eventslist/15">')
	self.assertIn(expected_input,escape(response.content))
	response = self.client.get('/eventslist/15')
	num_events = response.content.count('</tr>')
	self.assertEqual(num_events,15)
	expected_input = escape('<td>Concierto44</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<td>Concierto30</td>')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<a href="/eventslist/30">')
	self.assertIn(expected_input,escape(response.content))
	expected_input = escape('<a href="/eventslist/30">')
	self.assertIn(expected_input,escape(response.content))
	User.objects(username='john').delete()


	
class SearchFormTest(LiveServerTestCase):
    def _fixture_setup(self):
        c=Category(name='Musica')
        c.save()
	c=Category(name='Restauracion')
        c.save()
	user=User.create_user('john','john')
	request = HttpRequest() 
	user=User.objects(username='john')
	self.client.login(username='john',password='john')
 
    def _fixture_teardown(self):
        Category.objects.all().delete()
        Event.objects.all().delete()
	self.client.logout()
        User.objects(username='john').delete()  
        
    def test_search_form_load_categories_from_db(self):
        response = self.client.get('/eventslist/searchevents')
        for c in Category.objects().all() :   
            self.assertIn('<option value="'+c.name+'">'+c.name+'</option>',response.content.decode())        

    def test_validation_errors_are_sent_back_to_searchevents_template(self):
        response = self.client.post('/eventslist/searchevents')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventslist/searchevents.html')
        expected_error = escape("This field is required.")
        self.assertContains(response, expected_error)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/eventslist/searchevents',data={'title': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'})
	self.assertIsInstance(response.context['form'], SearchForm)
	expected_input = escape('Ensure this value has at most 30 characters (it has 34)')
        self.assertIn(expected_input,escape(response.content)) 


    def test_form_validation_for_blank_location(self):
        response = self.client.post('/eventslist/searchevents',data={'title': '','category': '','lat': '','lng': '','distance': ''}) 
        expected_input = escape('You must select a location')
	self.assertIn(expected_input,escape(response.content))

    def test_form_validation_for_right_distance(self):
        response = self.client.post('/eventslist/searchevents',data={'title': '','category': '','lat': '2','lng': '2','distance': '200'}) 
        expected_input = escape('Distance must be between 1 and 100')
	self.assertIn(expected_input,escape(response.content))
        
class AddCommentTest(LiveServerTestCase):
    def _fixture_setup(self):
        c=Category(name='Musica')
        c.save()
	c=Category(name='Restauracion')
        c.save()
        user=User.create_user('john','john')
	request = HttpRequest() 
	user=User.objects(username='john')
	self.client.login(username='john',password='john')
         
        
    def _fixture_teardown(self):
        Category.objects.all().delete()
        Event.objects.all().delete()
	self.client.logout()
        User.objects(username='john').delete()  
    
    def test_addcomment_requires_login_user(self):
	self.client.logout()
	response = self.client.get('/eventslist/addcomment',follow=True)
	self.assertEqual(response.status_code,200)
	self.assertRedirects(response,'/eventslist/login?next=/eventslist/addcomment')
    
    def test_addcomment_link_resolves_addcomment_view(self):
	page=resolve('/eventslist/addcomment')
	self.assertEqual(page.func, addcomment)
    
    def test_addcomment_page_uses_addcomment_form(self):
	response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category': 'Musica','lat':'49.8','lng':'4.7'})
	response = self.client.post('/eventslist/addcomment',data={'event_id': str(Event.objects(title='Concierto')[0].id)})
	self.assertIsInstance(response.context['form'], CommentForm, )

    def test_addcomment_page_save_comment_to_database(self):
	response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category': 'Musica','lat':'49.8','lng':'4.7'})
	response = self.client.post('/eventslist/addcomment',data={'content':'Esto es un comentario','event_id': str(Event.objects(title='Concierto')[0].id)}) 
	self.assertEqual(Event.objects(title='Concierto').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto')),'[<Event: Concierto-49.84.7-Es un concierto-Musica>]')
	self.assertEqual(str(Event.objects(title='Concierto')[0].comments[0]),'Esto es un comentario')
	

    def test_comments_are_in_home_page(self):
	response = self.client.post('/eventslist/addevent',data={'title': 'Concierto','description': 'Es un concierto','category': 'Musica','lat':'49.8','lng':'4.7'})
	response = self.client.post('/eventslist/addcomment',data={'content':'Esto es un comentario','event_id': str(Event.objects(title='Concierto')[0].id)}) 
	self.assertEqual(Event.objects(title='Concierto').count(),1) 
	self.assertEqual(str(Event.objects(title='Concierto')),'[<Event: Concierto-49.84.7-Es un concierto-Musica>]')
	response = self.client.get('/')  
	expected_html='Esto es un comentario'
	self.assertIn(expected_html,response.content)
	

















