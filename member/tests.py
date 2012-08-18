"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
import owtforum


class SimpleTest(TestCase):

    def test_owtforum_login(self):
        self.assertEqual(owtforum.check_password("user000", "user000p"),54)
        self.assertEqual(owtforum.check_password("user000", "bad_password"),-1)
        self.assertEqual(owtforum.check_password("bad_id", "bad_password"),-1)

    def test_dec64(self):
        enc64="qf0GuHjVxLaXDL/R59/6I2xOOk/bZyzrWS4x7eR/6uRqPk8DzTXwGjPqOA36+0WOaimqf+XcTv2OL5IUimPyoA=="
        self.assertEqual(owtforum.DEC64(enc64),"abcd")
        
    def test_enc64(self):
        data = "abcd"
        enc64=owtforum.ENC64(data)
        self.assertEqual(owtforum.DEC64(enc64),data)

        data = ""
        while len(data)<100:
            enc64=owtforum.ENC64(data)
            self.assertEqual(owtforum.DEC64(enc64),data)
            data += "x"

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
