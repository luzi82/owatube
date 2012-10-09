from django import forms
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import urllib
from django.contrib.auth.models import User
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
import game.swf
import magic
import pprint
import game.models as models

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
            db_game = game.models.Game.objects.get(pk = game_entry)
            return f(request,*args,db_game=db_game,**kwargs)
        except game.models.Game.DoesNotExist:
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

get_game_list_select_map={
    "comment_count" : 'SELECT COUNT(*) FROM game_gamecomment WHERE game_gamecomment.game_id = game_game.id',
    "report_count"  : 'SELECT COUNT(*) FROM game_scorereport WHERE game_scorereport.game_id = game_game.id',
}

@_check_u
def get_game_list(request, user):
    db_game_list = game.models.Game.objects.filter(author__exact=user).extra(select=get_game_list_select_map,)
    db_gamediff_list = game.models.GameDiff.objects.filter(game__in=db_game_list).select_related("game")
    game_map = {}
    for db_game in db_game_list:
        g = {}
        for k in ["id","title","create_date","comment_count","report_count"]:
            g[k] = getattr(db_game,k)
        g["star"]=game.create_empty_star_list()
        game_map[g["id"]]=g
    for db_gamediff in db_gamediff_list :
        game_id = db_gamediff.game.id
        ura_idx = 1 if db_gamediff.ura else 0
        diff_idx = db_gamediff.diff
        star = db_gamediff.star
        game_map[game_id]["star"][ura_idx][diff_idx] = star
    return render(request,"game/get_game_list.tmpl",{"game_list":game_map.values(),"list_user":user,"is_me":request.user==user})

@_check_game_entry
def get_game(request, db_game):
    comment_form = AddGameCommentForm(initial={"game_entry":db_game.id})
    
    comment_list=[]
    
    db_gamecomment_list = models.GameComment.objects.filter(game=db_game).order_by("-id")
    for db_gamecomment in db_gamecomment_list:
        comment_list.append({
            "author":db_gamecomment.player.username,
            "content":db_gamecomment.content,
            "datetime":db_gamecomment.create_date
        })
    
    return render(request,"game/get_game.tmpl",{
        "game":db_game,
        "comment_form":comment_form,
        "comment_list":comment_list
    })

@_check_game_entry
def get_game_data(request, db_game):
    return HttpResponse(FileWrapper(db_game.data),content_type="text/plain")

@_check_game_entry
def get_game_bgm(request, db_game):
    return HttpResponse(FileWrapper(db_game.bgm),content_type="audio/mpeg")

@_check_game_entry
def get_game_swf(request, db_game):
    return HttpResponse(
        FileWrapper(open("%(root)s/res/%(id)s.swf"%{"root":settings.OWATUBE_PATH,"id":db_game.swf},"r")),
        content_type="application/x-shockwave-flash"
    )

@login_required
def add_game_comment(request):
    if request.method == "POST":
        comment_form = AddGameCommentForm(request.POST)
        if comment_form.is_valid():
            game_entry = comment_form.cleaned_data["game_entry"]
            game_data = game.models.Game.objects.get(pk=game_entry)
            comment = comment_form.cleaned_data["comment"]
            comment = comment.encode("utf-8")
            comment = comment.strip()
            
            game.models.GameComment.objects.create(
                game = game_data,
                player = request.user,
                content = comment,
            )
                    
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
            db_game = game.models.Game.objects.create(
                author=request.user,
                state=models.GAME_STATE_EDIT,
            )
            
            form.to_db(db_game, request)
            
            return HttpResponseRedirect(reverse("game.views.edit_game",kwargs={"game_entry":db_game.id}))
            
    else:
        form = AddGameForm(initial={"id":-1})

    return render(request,"game/add_game.tmpl",{"form" : form})

@login_required
@_check_game_entry
def edit_game(request, db_game):
    if request.user != db_game.author :
        # TODO give error
        return HttpResponseRedirect(reverse("game.views.index"))
    
    if request.method == "POST":
        form = AddGameForm(request.POST, request.FILES)
        if form.is_valid():
            form.to_db(db_game, request)

    form = AddGameForm(initial={"id":db_game.id})
    submit_form = SubmitGameForm(initial={"id":db_game.id})
    game_star = game.get_game_star(db_game)
    
    return render(request,"game/edit_game.tmpl",{
        "form" : form,
        "submit_form" : submit_form,
        "title" : db_game.title,
        "music_by" : db_game.music_by,
        "data_by" : db_game.data_by,
        "star" : game_star,
        "game_id" : db_game.id
    })

class AddGameForm (forms.Form):
    id = forms.IntegerField(widget=forms.widgets.HiddenInput())
    data = forms.FileField(required=False)
    bgm = forms.FileField(required=False)
    swf = forms.ChoiceField(choices=game.swf.SWF_CHOICE)
    # pic
    
    def clean_data(self):
        data = self.cleaned_data['data'];
        
        if self.cleaned_data['id'] != -1 and data == None:
            return data
        if data == None:
            raise forms.ValidationError("No file")
        
        data.open()
        buf=data.read()

        ms = magic.open(magic.MAGIC_MIME_TYPE)
        ms.load()
        t=ms.buffer(buf)
        ms.close()

        if(t!="text/plain"):raise forms.ValidationError("Not text file")
        
        return data
    
    def clean_bgm(self):
        bgm = self.cleaned_data['bgm'];
        
        if self.cleaned_data['id'] != -1 and bgm == None:
            return bgm
        if bgm == None:
            raise forms.ValidationError("No file")
        
        bgm.open()
        buf=bgm.read()

        ms = magic.open(magic.MAGIC_MIME_TYPE)
        ms.load()
        t=ms.buffer(buf)
        ms.close()

        if(t!="audio/mpeg"):raise forms.ValidationError("Not mp3 file")
        
        return bgm

    def to_db(self,db_game,request):
        swf_key = self.cleaned_data["swf"]
        db_game.swf = swf_key

        data_f=self.cleaned_data["data"]
        if data_f != None:
            data_f.open()
            data_buf = data_f.read()
            data_data = game.swf.parse_data(swf_key, data_buf)
            db_game.title = data_data["title"]
            db_game.music_by = data_data["music_by"]
            db_game.data_by=data_data["data_by"]
            db_game.data=request.FILES['data']
            game.models.GameDiff.objects.filter(
                game = db_game,
                ura = False,
            ).delete()
            for i in range(len(data_data["diff"])):
                star = data_data["diff"][i]
                if star == 0 : continue
                game.models.GameDiff.objects.create(
                    game = db_game,
                    ura = False,
                    diff = i,
                    star = star,
                )
            
        bgm_f = self.cleaned_data["bgm"]
        if bgm_f != None:
            db_game.bgm = request.FILES['bgm']

        db_game.save()

@login_required
def submit_game(request):
    if request.method != "POST":
        # TODO give error
        return HttpResponseRedirect(reverse("game.views.index"))

    form = SubmitGameForm(request.POST)
    if not form.is_valid():
        # TODO give error
        return HttpResponseRedirect(reverse("game.views.index"))
    
    game_id = form.cleaned_data["id"]
    
    db_game = game.models.Game.objects.get(pk = game_id)
    if db_game.author != request.user:
        # TODO give error
        return HttpResponseRedirect(reverse("game.views.index"))
    if db_game.state != models.GAME_STATE_EDIT:
        # TODO give error
        return HttpResponseRedirect(reverse("game.views.index"))
    
    db_game.state = models.GAME_STATE_PUBLIC
    db_game.save()
    
    return HttpResponseRedirect(reverse("game.views.get_game",kwargs={"game_entry":db_game.id}))

class SubmitGameForm (forms.Form):
    id = forms.IntegerField(widget=forms.widgets.HiddenInput())



