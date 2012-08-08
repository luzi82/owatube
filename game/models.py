from django.db import models
from django.contrib.auth import models as auth_models

class Game(models.Model):
    author = models.ForeignKey(auth_models.User)
    create_date = models.DateTimeField()
