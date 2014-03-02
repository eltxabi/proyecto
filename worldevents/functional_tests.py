from selenium import webdriver
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

      #We can see a registration form 
      reg_form=self.browser.find_element_by_name('Registration_Form')
      self.assertNotEquals(reg_form,None)


	     

if __name__ == '__main__':  
   unittest.main()  


