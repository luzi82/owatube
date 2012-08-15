from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request,"index.tmpl")

def get_game_list_fw(request):
    return render(request,"dummy.tmpl")

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
