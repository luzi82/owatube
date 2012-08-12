"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
import pprint


class SimpleTest(TestCase):

    def test_basic_reg(self):
        c = Client()
        response = c.post("/member/register/",{"username":"hellouser","password0":"hellopass","password1":"hellopass"},follow=True)
        self.assertRedirects(response,"/member/register_success/")

    def test_short_username(self):
        c = Client()
        response = c.post("/member/register/",{"username":"h","password0":"hellopass","password1":"hellopass"},follow=False)
#        self.assertEqual(response.template, second, msg)
        self.assertEqual(response.status_code, 200)
#        pprint.pprint(response.template)
