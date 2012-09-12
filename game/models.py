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
    game = models.ForeignKey(Game)
    diff = models.IntegerField()
    star = models.IntegerField()

class ScoreReport(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(auth_models.User)
    diff = models.IntegerField()
    ura = models.BooleanField()
    success = models.BooleanField()
    r0 = models.IntegerField()
    r1 = models.IntegerField()
    r2 = models.IntegerField()
    maxcombo = models.IntegerField()
    lenda = models.IntegerField()
    code = models.IntegerField()
    original = models.TextField(max_length=1000)
