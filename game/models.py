from django.db import models
from django.contrib.auth import models as auth_models

class Game(models.Model):
    author = models.ForeignKey(auth_models.User)
    create_date = models.DateTimeField(auto_now=True)
    data = models.FileField(upload_to="game/data/%Y/%m/%d")
    bgm = models.FileField(upload_to="game/bgm/%Y/%m/%d")
    swf = models.CharField(max_length=8)
