from django.test.simple import DjangoTestSuiteRunner
from django.test import TestCase
from django.core.urlresolvers import resolve
from eventslist.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

from eventslist.models import Entrada

class HomePageTest(TestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        pass

    def test_root_resolves_home_page_view(self):
	page=resolve('/')
	self.assertEqual(page.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest() 
        response = home_page(request)  
        expected_html = render_to_string('eventslist/home.html')
        self.assertEqual(response.content.decode(), expected_html)




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








