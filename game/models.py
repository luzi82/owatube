from django.db import models
from django.contrib.auth import models as auth_models

class Game(models.Model):
    author = auth_models.User
