from django import forms
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from game.models import Game
import urllib
from django.contrib.auth.models import User

## helper function

def _check_u(f):
    def ff(request,*args,**kwargs):
        username=request.GET.get("u",None)
        if username!=None:
            try:
                user = User.objects.get(username__exact = username)
                return f(request,*args,user=user,**kwargs)
            except User.DoesNotExist:
                return HttpResponseRedirect(reverse("game.views.index"))
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("game.views.index"))
        p = {"u":request.user.username}
        return HttpResponseRedirect(request.path+"?"+urllib.urlencode(p))
    return ff

# view func

def index(request):
    return render(request,"game/index.tmpl")

@_check_u
def get_user_profile(request,user):
    return render(request,"dummy.tmpl")

@_check_u
def get_game_score_list(request, user):
    return render(request,"dummy.tmpl")

@_check_u
def get_game_list(request, user):
    game_list = Game.objects.filter(author__exact=user)
    return render(request,"game/get_game_list.tmpl",{"game_list":game_list})

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

