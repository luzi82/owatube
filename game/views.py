from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request,"index.tmpl")

def get_game_list(request):
    return HttpResponse("dummy")

def get_game(request):
    return HttpResponse("dummy")

def add_game_comment(request):
    return HttpResponse("dummy")

def add_game_score(request):
    return HttpResponse("dummy")

def add_game_rank(request):
    return HttpResponse("dummy")

def add_game(request):
    return HttpResponse("dummy")

def edit_game(request):
    return HttpResponse("dummy")
