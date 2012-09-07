from django import forms
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from game.models import Game
import urllib
from django.contrib.auth.models import User
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
import game.swf
import pprint
import magic
import django.core.files.uploadedfile

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

def _check_game_entry(f):
    def ff(request,game_entry,*args,**kwargs):
        try:
            game = Game.objects.get(pk = game_entry)
            return f(request,*args,game=game,**kwargs)
        except Game.DoesNotExist:
            return HttpResponseRedirect(reverse("game.views.index"))
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

@_check_game_entry
def get_game(request, game):
    comment_form = AddGameCommentForm(initial={"game_entry":game.id})
    return render(request,"game/get_game.tmpl",{"game":game,"comment_form":comment_form})

@_check_game_entry
def get_game_data(request, game):
    return HttpResponse(FileWrapper(game.data),content_type="text/plain")

@_check_game_entry
def get_game_bgm(request, game):
    return HttpResponse(FileWrapper(game.bgm),content_type="audio/mpeg")

@_check_game_entry
def get_game_swf(request, game):
    return HttpResponse(
        FileWrapper(open("%(root)s/res/%(id)s.swf"%{"root":settings.OWATUBE_PATH,"id":game.swf},"r")),
        content_type="application/x-shockwave-flash"
    )

@login_required
def add_game_comment(request):
    if request.method == "POST":
        comment_form = AddGameCommentForm(request.POST)
        if comment_form.is_valid():
            game_entry = comment_form.cleaned_data["game_entry"]
            comment = comment_form.cleaned_data["comment"]
            return HttpResponseRedirect(reverse("game.views.get_game",kwargs={"game_entry":game_entry}))
    return HttpResponseRedirect(reverse("game.views.index"))

class AddGameCommentForm (forms.Form):
    game_entry = forms.CharField(widget=forms.widgets.HiddenInput())
    comment = forms.CharField(widget=forms.widgets.Textarea())

@login_required
def add_game_rank(request):
    return render(request,"dummy.tmpl")

@login_required
def add_game(request):
    if request.method == "POST":
        form = AddGameForm(request.POST, request.FILES)
        if form.is_valid():
            game = Game(author=request.user,data=request.FILES['data'],bgm=request.FILES['bgm'],swf=form.cleaned_data["swf"])
            game.save()
            return HttpResponseRedirect(reverse("game.views.get_game",kwargs={"game_entry":game.pk}))
    else:
        form = AddGameForm()
    return render(request,"game/add_game.tmpl",{"form":form})

class AddGameForm (forms.Form):
    data = forms.FileField()
    bgm = forms.FileField()
    swf = forms.ChoiceField(choices=game.swf.SWF_CHOICE)
    # pic
    
    def clean_data(self):
        data = self.cleaned_data['data']
        buf=data.read()

        ms = magic.open(magic.MAGIC_MIME_TYPE)
        ms.load()
        t=ms.buffer(buf)
        ms.close()

        if(t!="text/plain"):raise forms.ValidationError("Not text file")
        
        return data
    
    def clean_bgm(self):
        bgm = self.cleaned_data['bgm']
        buf=bgm.read()

        ms = magic.open(magic.MAGIC_MIME_TYPE)
        ms.load()
        t=ms.buffer(buf)
        ms.close()

        if(t!="audio/mpeg"):raise forms.ValidationError("Not mp3 file")
        
        return bgm

@login_required
def edit_game(request, game_entry):
    return render(request,"dummy.tmpl")

