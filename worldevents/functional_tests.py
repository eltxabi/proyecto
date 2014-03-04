from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):  

   def setUp(self):  
      self.browser = webdriver.Firefox()
      self.browser.implicitly_wait(3)

   def tearDown(self):  
      self.browser.quit()

   def test_see_main_page(self):  
      # Check out homepage
      self.browser.get('http://localhost:8000')

      # The page title mention WorldEvents
      self.assertIn('WorldEvents', self.browser.title)  
      self.fail('Finish the test!')  
   
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




if __name__ == '__main__':  
    unittest.main()       


