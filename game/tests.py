"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    
    def test_param_pass(self):
        def A(a,b,c):
            return a+b+c
        def B(a,*args,**kwargs):
            return A(a,2,*args,**kwargs)
        def C(a,*args,**kwargs):
            return A(a,*args,c=4,**kwargs)
        self.assertEqual(B(1,c=4),7)
        self.assertEqual(B(1,4),7)
        self.assertEqual(C(1,b=2),7)
        self.assertEqual(C(1,2),7)
