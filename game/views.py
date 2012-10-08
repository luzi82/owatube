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
            game_data = game.models.Game.objects.get(pk = game_entry)
            return f(request,*args,game=game_data,**kwargs)
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
for u in xrange(2):
    for d in xrange(4):
        m={"u":u,"d":d}
        get_game_list_select_map["d%(u)d%(d)d"%m]="""
            CASE
                WHEN EXISTS (
                    SELECT * FROM game_gamediff
                        WHERE
                            game_gamediff.game_id = game_game.id AND
                            game_gamediff.ura = %(u)d AND
                            game_gamediff.diff = %(d)d
                    ) 
                    THEN (
                        SELECT star FROM game_gamediff
                            WHERE
                                game_gamediff.game_id = game_game.id AND
                                game_gamediff.ura = %(u)d AND
                                game_gamediff.diff = %(d)d
                    )
                ELSE "-"
            END
        """%m

@_check_u
def get_game_list(request, user):
    game_list = game.models.Game.objects.filter(author__exact=user).extra(select=get_game_list_select_map,)
    return render(request,"game/get_game_list.tmpl",{"game_list":game_list,"list_user":user,"is_me":request.user==user})

@_check_game_entry
def get_game(request, game):
    comment_form = AddGameCommentForm(initial={"game_entry":game.id})
    
    comment_list=[]
    
    db_gamecomment_list = models.GameComment.objects.filter(game=game).order_by("-id")
    for db_gamecomment in db_gamecomment_list:
        comment_list.append({
            "author":db_gamecomment.player.username,
            "content":db_gamecomment.content,
            "datetime":db_gamecomment.create_date
        })
    
    return render(request,"game/get_game.tmpl",{
        "game":game,
        "comment_form":comment_form,
        "comment_list":comment_list
    })

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
            game_id = form.cleaned_data["id"]
            if game_id == -1:
                db_game = game.models.Game.objects.create(
                    author=request.user,
                    state=models.GAME_STATE_EDIT,
                )
                game_id = db_game.id
            else:
                db_game = game.models.Game.objects.get(pk = game_id)
                if db_game.author != request.user:
                    # TODO give error
                    return HttpResponseRedirect(reverse("game.views.index"))
                if db_game.state != models.GAME_STATE_EDIT:
                    # TODO give error
                    return HttpResponseRedirect(reverse("game.views.index"))

            swf_key = form.cleaned_data["swf"]
            db_game.swf = swf_key

            data_f=form.cleaned_data["data"]
            if data_f != None:
                data_f.open()
                data_buf = data_f.read()
                data_data = game.swf.parse_data(swf_key, data_buf)
                db_game.title = data_data["title"]
                db_game.music_by = data_data["music_by"]
                db_game.data_by=data_data["data_by"]
                db_game.data=request.FILES['data']
                
            bgm_f = form.cleaned_data["bgm"]
            if bgm_f != None:
                db_game.bgm = request.FILES['bgm']

#            for i in range(len(data_data["diff"])):
#                star = data_data["diff"][i]
#                if star==0:continue
#                game.models.GameDiff.objects.create(
#                    game = db_game,
#                    ura = False,
#                    diff = i,
#                    star = star,
#                )
#            return HttpResponseRedirect(reverse("game.views.get_game",kwargs={"game_entry":db_game.pk}))

            db_game.save()
            
            form = AddGameForm(initial={
                "id":game_id,
                "swf":swf_key,
            })
    else:
        form = AddGameForm(initial={"id":-1})
    return render(request,"game/add_game.tmpl",{"form":form})

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

@login_required
def edit_game(request, game_entry):
    return render(request,"dummy.tmpl")

