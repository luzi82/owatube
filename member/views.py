from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.core.urlresolvers import reverse

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("member.views.register_success"))
    else:
        form = RegisterForm()
    return render(request,"register.tmpl",{"form":form})

def register_success(request):
    return render(request,"register_success.tmpl")

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20,min_length=6)
    password0 = forms.CharField(widget=forms.PasswordInput(),min_length=6)
    password1 = forms.CharField(widget=forms.PasswordInput(),min_length=6)

    def clean_password1(self):
        password0 = self.cleaned_data['password0']
        password1 = self.cleaned_data['password1']
        
        if password0 != password1:
            del self.cleaned_data['password0']
            del self.cleaned_data['password1']
            raise forms.ValidationError("ValidationError")
        
        return password0
