"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client


class SimpleTest(TestCase):

    pass

#    def test_basic_reg(self):
#        c = Client()
#
#        self.assertFalse(c.login(username="hellouser",password="hellopass"))
#
#        response = c.post("/member/register/",{"username":"hellouser","password0":"hellopass","password1":"hellopass"},follow=True)
#        self.assertRedirects(response,"/member/register_success/")
#        self.assertEqual(response.templates[0].name, "member/register_success.tmpl")
#        
#        self.assertTrue(c.login(username="hellouser",password="hellopass"))
#        
#    def test_err_short_username(self):
#        c = Client()
#        response = c.post("/member/register/",{"username":"h","password0":"hellopass","password1":"hellopass"},follow=False)
##        self.assertEqual(response.template, second, msg)
#        self.assertEqual(response.status_code, 200)
#        self.assertEqual(response.templates[0].name, "member/register.tmpl")
#        self.assertFormError(response, "form", "username", None)
#
#    def test_err_double_username_reg(self):
#        c = Client()
#        
#        response = c.post("/member/register/",{"username":"hellouser","password0":"hellopass","password1":"hellopass"},follow=False)
#        self.assertRedirects(response,"/member/register_success/")
#        
#        response = c.post("/member/register/",{"username":"hellouser","password0":"hellopass","password1":"hellopass"},follow=False)
#
#        self.assertEqual(response.status_code, 200)
#        self.assertEqual(response.templates[0].name, "member/register.tmpl")
#        self.assertFormError(response, "form", "username", None)
#
#    def test_err_password_unequal(self):
#        c = Client()
#        
#        response = c.post("/member/register/",{"username":"hellouser","password0":"hellopass","password1":"hellopasss"},follow=False)
#
#        self.assertEqual(response.status_code, 200)
#        self.assertEqual(response.templates[0].name, "member/register.tmpl")
#        self.assertFormError(response, "form", "password1", None)
