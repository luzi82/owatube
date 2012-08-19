from django import forms
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from game.models import Game
import urllib

## helper function

def _check_u(f):
    def ff(request,*args,**kwargs):
        username=_get_user(request)
        if username!=None:return f(request,*args,username=username,**kwargs)
        if not request.user.is_authenticated():
            HttpResponseRedirect(reverse("game.views.index"))
        p = {"u":request.user.username}
        return HttpResponseRedirect(request.path+"?"+urllib.urlencode(p))
    return ff

# view func

def index(request):
    return render(request,"game/index.tmpl")

@_check_u
def get_user_profile(request,username):
    return render(request,"dummy.tmpl",{"msg":username})

@_check_u
def get_game_score_list(request, username):
    return render(request,"dummy.tmpl")

@_check_u
def get_game_list(request, username):
    return render(request,"dummy.tmpl")

def get_game(request, game_entry):
    return render(request,"dummy.tmpl")

@login_required
def add_game_comment(request):
    return render(request,"dummy.tmpl")

@login_required
def add_game_score(request):
    return render(request,"dummy.tmpl")

@login_required
def add_game_rank(request):
    return render(request,"dummy.tmpl")

@login_required
def add_game(request):
    if request.method == "POST":
        form = AddGameForm(request.POST, request.FILES)
        if form.is_valid():
            game = Game(author=request.user,data=request.FILES['data'],bgm=request.FILES['bgm'])
            game.save()
            return HttpResponseRedirect(reverse("game.views.get_game",kwargs={"game_entry":game.pk}))
    else:
        form = AddGameForm()
    return render(request,"game/add_game.tmpl",{"form":form})

class AddGameForm (forms.Form):
    data = forms.FileField()
    bgm = forms.FileField()
    # owata_ver
    # pic

@login_required
def edit_game(request, game_entry):
    return render(request,"dummy.tmpl")


######

def _get_user(request):
    return request.GET.get("u",None)
