from django.db import models
from django.contrib.auth import models as auth_models
from django.conf import settings

GAME_STATE_EDIT = 0
GAME_STATE_PUBLIC = 1
GAME_STATE_DEL = 2
GAME_STATE_DEPREDICTED = 3

class Game(models.Model):
    author = models.ForeignKey(auth_models.User,db_index=True)
    title = models.CharField(max_length=settings.OWATA_TITLE_SIZE,null=True)
    music_by = models.CharField(max_length=settings.OWATA_MUSICBY_SIZE,null=True)
    data_by = models.CharField(max_length=settings.OWATA_DATABY_SIZE,null=True)
    create_date = models.DateTimeField(auto_now=True)
    data = models.FileField(upload_to="game/data/%Y/%m/%d",null=True)
    bgm = models.FileField(upload_to="game/bgm/%Y/%m/%d",null=True)
    swf = models.CharField(max_length=8,null=True)
    state = models.IntegerField(db_index=True)
    successor = models.ForeignKey("self",null=True)

class GameDiff(models.Model):
    game = models.ForeignKey(Game,db_index=True)
    ura = models.BooleanField(db_index=True)
    diff = models.IntegerField(db_index=True)
    star = models.IntegerField()
    
class GameComment(models.Model):
    game = models.ForeignKey(Game,db_index=True)
    create_date = models.DateTimeField(auto_now=True,db_index=True)
    player = models.ForeignKey(auth_models.User,db_index=True)
    content = models.TextField()

class ScoreReport(models.Model):
    game = models.ForeignKey(Game,db_index=True)
    create_date = models.DateTimeField(auto_now=True,db_index=True)
    player = models.ForeignKey(auth_models.User,db_index=True)
    diff = models.IntegerField(db_index=True)
    ura = models.BooleanField(db_index=True)
    success = models.BooleanField()
    score = models.IntegerField(db_index=True)
    r0 = models.IntegerField()
    r1 = models.IntegerField()
    r2 = models.IntegerField()
    maxcombo = models.IntegerField()
    lenda = models.IntegerField()
    
class ScoreReportBest(models.Model):
    report = models.ForeignKey(ScoreReport,db_index=True)
