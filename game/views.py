from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from game.models import Game

def index(request):
    return render(request,"game/index.tmpl")

def get_user_profile_fw(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("game.views.index"))
    return HttpResponseRedirect(reverse("game.views.get_user_profile",kwargs={"username":request.user.username}))

def get_user_profile(request, username):
    return render(request,"dummy.tmpl")

def get_game_score_list_fw(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("game.views.index"))
    return HttpResponseRedirect(reverse("game.views.get_game_score_list",kwargs={"username":request.user.username}))

def get_game_score_list(request, username):
    return render(request,"dummy.tmpl")

def get_game_list_fw(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("game.views.index"))
    return HttpResponseRedirect(reverse("game.views.get_game_list",kwargs={"username":request.user.username}))

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
