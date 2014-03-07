from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import Connection
import unittest
from auth import PasswordUtils

class NewVisitorTest(unittest.TestCase):  

   def setUp(self):
      self.browser = webdriver.Firefox()
      self.browser.implicitly_wait(3)

   def tearDown(self):  
      self.browser.quit()
      #self.remove_user('mary')

   def test_can_login(self):
      # Adding user mary   
      self.add_user('mary','mary')	

      # Check out homepage
      self.browser.get('http://localhost:8000')

      # The page has a login link
      login_links=self.browser.find_elements_by_link_text('Login')
      self.assertEquals(len(login_links),1)
         	
      # Click in login link
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
      
      # Removing user mary   
      self.remove_user('mary')

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
      	
      # Removing user john 
      self.remove_user('john')	 	


   def test_see_main_page(self):  
      # Check out homepage
      self.browser.get('http://localhost:8000')

      # The page title mention WorldEvents
      self.assertIn('WorldEvents', self.browser.title)  
      self.fail('Finish the test!')  

   def test_can_add_event(self):
      # Adding user mary   
      self.add_user('mary','mary')
      
      # Login Mary
      self.login_user('mary')

      # Check out homepage
      self.browser.get('http://localhost:8000') 

      # The page has a addEvent link
      add_event_links=self.browser.find_elements_by_link_text('Add Event')
      self.assertEquals(len(add_event_links),1)
         	
      #Click in addEvent link
      add_event_links[0].click() 

      #I can see an addEvent form 
      title_input=self.browser.find_element_by_name('title')
      self.assertNotEquals(title_input,None)
      description_input=self.browser.find_element_by_name('description')
      self.assertNotEquals(description_input,None)
      category_select=self.browser.find_element_by_name('category')
      self.assertNotEquals(category_select,None)
      
      #I enter data
      title_input.send_keys('Prueba') 
      description_input.send_keys('Esto es una prueba')
      self.browser.find_element_by_css_selector('option[value=musica]').click() 
      self.browser.find_element_by_id('my_map').click()
      self.browser.find_element_by_css_selector('input[value=add]').click()  
	
      #I can see home page with success message
      messages=self.browser.find_element_by_id('messages')
      self.assertIn("Prueba has been created",messages.text) 

      #Removing event
      self.remove_event('Prueba') 

      #Removing user mary   
      self.remove_user('mary')

   def remove_event(self,titulo):
      con = Connection()	
      db = con['worldevents']
      events = db.event
      events.remove({'titulo':titulo})

   def add_user(self,username,password):
      con = Connection()	
      db = con['worldevents']
      users = db.user
      pu=PasswordUtils()
      hash_password=pu.make_password(password)
      users.insert({'username':username,'password':hash_password,"is_active" : True,"_cls" : "User"})	 

   def remove_user(self,username):
      con = Connection()	
      db = con['worldevents']
      users = db.user
      users.remove({'username':username})	
  
   def login_user(self,username):

      # Check out homepage
      self.browser.get('http://localhost:8000')

       # Click in login link
      login_links=self.browser.find_elements_by_link_text('Login')
      login_links[0].click() 
      
      # mary login
      username_input=self.browser.find_element_by_name('username')
      self.assertNotEquals(username_input,None)
      password_input=self.browser.find_element_by_name('password')
      self.assertNotEquals(password_input,None)
      username_input.send_keys('mary')
      password_input.send_keys('mary') 
      password_input.send_keys(Keys.ENTER)  
           
    
if __name__ == '__main__':  
    unittest.main()       


