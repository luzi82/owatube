from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.core.urlresolvers import reverse

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            HttpResponseRedirect(reverse("game.views.index"))
    else:
        form = RegisterForm()
    return render(request,"register.html",{"form":form})

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
