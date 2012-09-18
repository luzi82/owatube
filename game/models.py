from django.db import models
from django.contrib.auth import models as auth_models
from django.conf import settings

class Game(models.Model):
    author = models.ForeignKey(auth_models.User)
    title = models.CharField(max_length=settings.OWATA_TITLE_SIZE)
    music_by = models.CharField(max_length=settings.OWATA_MUSICBY_SIZE)
    data_by = models.CharField(max_length=settings.OWATA_DATABY_SIZE)
    create_date = models.DateTimeField(auto_now=True)
    data = models.FileField(upload_to="game/data/%Y/%m/%d")
    bgm = models.FileField(upload_to="game/bgm/%Y/%m/%d")
    swf = models.CharField(max_length=8)

class GameDiff(models.Model):
    game = models.ForeignKey(Game,db_index=True)
    diff = models.IntegerField(db_index=True)
    star = models.IntegerField()
    
class GameComment(models.Model):
    game = models.ForeignKey(Game,db_index=True)
    create_date = models.DateTimeField(auto_now=True,db_index=True)
    player = models.ForeignKey(auth_models.User,db_index=True)
    content = models.TextField()

class GameCommentContent(models.Model):
    parent = models.ForeignKey(GameComment,db_index=True)
    part = models.IntegerField()
    content = models.TextField()
    is_score = models.BooleanField()
    
class ScoreReport(models.Model):
    parent = models.ForeignKey(GameCommentContent,db_index=True)
    diff = models.IntegerField(db_index=True)
    ura = models.BooleanField(db_index=True)
    success = models.BooleanField()
    score = models.IntegerField(db_index=True)
    r0 = models.IntegerField()
    r1 = models.IntegerField()
    r2 = models.IntegerField()
    maxcombo = models.IntegerField()
    lenda = models.IntegerField()
    code = models.IntegerField()
    prove = models.CharField(max_length=64)
    
class ScoreReportBest(models.Model):
    report = models.ForeignKey(ScoreReport,db_index=True)
