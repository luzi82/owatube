from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import django.contrib.auth as auth

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username=form.cleaned_data["username"],password=form.cleaned_data["password0"])
            user = auth.authenticate(username=form.cleaned_data["username"],password=form.cleaned_data["password0"])
            if user.is_active:
                auth.login(request, user)
            return HttpResponseRedirect(reverse("member.views.register_success"))
    else:
        form = RegisterForm()
    return render(request,"member/register.tmpl",{"form":form})

def register_success(request):
    return render(request,"member/register_success.tmpl")

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20,min_length=6)
    password0 = forms.CharField(widget=forms.PasswordInput(),min_length=6)
    password1 = forms.CharField(widget=forms.PasswordInput(),min_length=6)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count():
            raise forms.ValidationError("User exists")
        
        return username

    def clean_password1(self):
        password0 = self.cleaned_data['password0']
        password1 = self.cleaned_data['password1']
        
        if password0 != password1:
            del self.cleaned_data['password0']
            del self.cleaned_data['password1']
            raise forms.ValidationError("ValidationError")
        
        return password0


def profile(request, username):
    return render(request,"dummy.tmpl")

