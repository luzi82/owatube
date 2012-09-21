# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import re
import game.swf
from django.contrib.auth.models import User
from django.test.client import Client

class SimpleTest(TestCase):
    
    def test_param_pass(self):
        def A(a,b,c):
            return a+b+c
        def B(a,*args,**kwargs):
            return A(a,2,*args,**kwargs)
        def C(a,*args,**kwargs):
            return A(a,*args,c=4,**kwargs)
        self.assertEqual(B(1,c=4),7)
        self.assertEqual(B(1,4),7)
        self.assertEqual(C(1,b=2),7)
        self.assertEqual(C(1,2),7)

    def test_add_game(self):
        User.objects.create_user("submitter",password="asdf")

        client = Client()
        client.login(username="submitter",password="asdf")
        
        data_f=open("game/test_res/data.txt","r")
        bgm_f=open("game/test_res/bgm.mp3","r")
        response = client.post("/game/upload/", {
            "data":data_f,
            "bgm":bgm_f,
            "swf":"f90626fa",
        })
        self.assertRedirects(response,"/g/1/")
        
        game_data = game.models.Game.objects.get(pk=1)
        self.assertEqual(game_data.title,u"凛として咲く花の如く")
        self.assertEqual(game_data.music_by,"")
        self.assertEqual(game_data.data_by,"No.31")

        try:
            game.models.GameDiff.objects.get(game=game_data,diff=0)
            self.fail()
        except game.models.GameDiff.DoesNotExist:pass

        try:
            game.models.GameDiff.objects.get(game=game_data,diff=1)
            self.fail()
        except game.models.GameDiff.DoesNotExist:pass

        try:
            game.models.GameDiff.objects.get(game=game_data,diff=2)
            self.fail()
        except game.models.GameDiff.DoesNotExist:pass
        
        tmp = game.models.GameDiff.objects.get(game=game_data,diff=3)
        self.assertEqual(tmp.star, 7)

    def test_add_game_data_err(self):
        User.objects.create_user("submitter",password="asdf")

        client = Client()
        client.login(username="submitter",password="asdf")
        
        data_f=open("game/test_res/bgm.mp3","r")
        bgm_f=open("game/test_res/bgm.mp3","r")
        response = client.post("/game/upload/", {
            "data":data_f,
            "bgm":bgm_f,
            "swf":"f90626fa",
        })
        self.assertTemplateUsed(response, "game/add_game.tmpl")

    def test_add_game_bgm_err(self):
        User.objects.create_user("submitter",password="asdf")

        client = Client()
        client.login(username="submitter",password="asdf")
        
        data_f=open("game/test_res/data.txt","r")
        bgm_f=open("game/test_res/data.txt","r")
        response = client.post("/game/upload/", {
            "data":data_f,
            "bgm":bgm_f,
            "swf":"f90626fa",
        })
        self.assertTemplateUsed(response, "game/add_game.tmpl")

    def test_parse_data(self):
        data_buf = open("game/test_res/data.txt","r").read()
        ret = game.swf.parse_data_0(data_buf)
        self.assertEqual(ret["title"], "凛として咲く花の如く")
        self.assertEqual(ret["music_by"], "")
        self.assertEqual(ret["data_by"], "No.31")
        self.assertEqual(ret["diff"], [0,0,0,7])


    def test_add_game_comment(self):
        User.objects.create_user("submitter",password="asdf")
        
        client = Client()
        client.login(username="submitter",password="asdf")
        
        data_f=open("game/test_res/data.txt","r")
        bgm_f=open("game/test_res/bgm.mp3","r")
        client.post("/game/upload/", {
            "data":data_f,
            "bgm":bgm_f,
            "swf":"f90626fa",
        })

        comment="Comment 1"
        client.post("/game/comment/", {
            "game_entry":"1",
            "comment":comment,
        })
        
        db_gamecomment=game.models.GameComment.objects.get(pk=1)
        self.assertEqual(db_gamecomment.player.username,"submitter")
        self.assertEqual(db_gamecomment.content,comment.decode("utf-8"))
