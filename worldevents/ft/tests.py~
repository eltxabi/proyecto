from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import Connection
import unittest
from mongoengine.django.auth import User

class NewVisitorTest(unittest.TestCase):  

   def setUp(self): 
      User.create_user('mary','mary')
      self.browser = webdriver.Firefox()
      self.browser.implicitly_wait(3)

   def tearDown(self):  
      self.browser.quit()
      User.objects.filter(username='mary').delete()
     
   def test_can_login(self):
      # Check out homepage
      self.browser.get(self.live_server_url)

      # The page has a login link
      login_links=self.browser.find_elements_by_link_text('Login')
      self.assertEquals(len(login_links),1)
         	
      #Click in login link
      login_links[0].click() 

      # The page has a login form
      username_input=self.browser.find_element_by_name('username')
      self.assertNotEquals(username_input,None)
      password_input=self.browser.find_element_by_name('password')
      self.assertNotEquals(password_input,None)
      login_button=self.browser.find_elements_by_css_selector('form input[value="login"]')
      self.assertNotEquals(login_button,None)

      # mary login
      username_input.send_keys('mary')
      password_input.send_keys('mary') 
      password_input.send_keys(Keys.ENTER)  

      # I can see login correct advice
      self.assertIn('Login correcto mary', self.browser.page_source)


   def test_can_register(self):
      # Check out homepage
      self.browser.get('http://localhost:8000')
       
      # The page has a registration link
      register_links=self.browser.find_elements_by_link_text('Registro')
      self.assertEquals(len(register_links),1)
         	
      #Click in registration link
      register_links[0].click() 

      #I can see a registration form 
      username_input=self.browser.find_element_by_name('username')
      self.assertNotEquals(username_input,None)
      password1_input=self.browser.find_element_by_name('password1')
      self.assertNotEquals(password1_input,None)
      password2_input=self.browser.find_element_by_name('password2')
      self.assertNotEquals(password2_input,None)
	
      #I enter this data: username->john,password->john
      username_input.send_keys('john')
      password1_input.send_keys('john') 
      password2_input.send_keys('john') 
      password2_input.send_keys(Keys.ENTER)  

      #I can see home page with success message
      messages=self.browser.find_element_by_id('messages')
      self.assertIn("you have been successfully registered",messages.text)	 	


   def test_see_main_page(self):  
      # Check out homepage
      self.browser.get('http://localhost:8000')

      # The page title mention WorldEvents
      self.assertIn('WorldEvents', self.browser.title)  
      self.fail('Finish the test!')  
  
  
