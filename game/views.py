from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

def index(request):
    return render(request,"index.tmpl")

def get_game_list_fw(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("game.views.index"))
    return HttpResponseRedirect(reverse("game.views.get_game_list",kwargs={"username":request.user.username}))

def get_game_list(request, username):
    return render(request,"dummy.tmpl")

def get_game(request, game_entry):
    return render(request,"dummy.tmpl")

def add_game_comment(request):
    return render(request,"dummy.tmpl")

def add_game_score(request):
    return render(request,"dummy.tmpl")

def add_game(request):
    return render(request,"dummy.tmpl")

def edit_game(request, game_entry):
    return render(request,"dummy.tmpl")
