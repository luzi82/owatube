# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import re
import game.swf.code0
import game.swf.code1
import game.swf
from django.contrib.auth.models import User
from django.test.client import Client
import pprint

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

    def test_reg(self):
        text="*太鼓のオワタツジン結果*Ver3.03"
        reg="\*太鼓のオワタツジン結果\*Ver3\.03"
        self.assertTrue(re.match(reg,text))

        text="""*太鼓のオワタツジン結果*Ver3.03
曲名:凛として咲く花の如く"""
        reg="""\*太鼓のオワタツジン結果\*Ver3\.03
曲名:([^\\n]*)"""
        m=re.search(reg,text)
        self.assertEqual(m.group(1),"凛として咲く花の如く")
        
        text="""*太鼓のオワタツジン結果*Ver3.03
曲名:凛として咲く花の如く
曲:
譜面:No.31
コース:おわたコース(★7)
ノルマクリア成功
得点:1026720点
判定:良 573/可 0/不可 0
最大コンボ数:573回
叩けた率:100%
連打:118回
オプション:なし
譜面コード:16906247
証明コード:
#!#16906247!#1026720!#31345!#15589489!#23726650!#"""
        m=game.swf.parse_report_0_re0.search(text)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("success"),"成功")
        self.assertEqual(m.group("score"),"1026720")
        self.assertEqual(m.group("r0"),"573")
        self.assertEqual(m.group("r1"),"0")
        self.assertEqual(m.group("r2"),"0")
        self.assertEqual(m.group("maxcombo"),"573")
        self.assertEqual(m.group("lenda"),"118")
        self.assertEqual(m.group("option"),"なし")
        self.assertEqual(m.group("code"),"16906247")
        self.assertEqual(m.group("prove"),"#!#16906247!#1026720!#31345!#15589489!#23726650!#")
        
        m2=game.swf.parse_report_0_re1.search(m.group("prove"))
        self.assertEqual(m2.group("code"),"16906247")
        self.assertEqual(m2.group("score"),"1026720")

    def test_comment_parse(self):
        text="""*太鼓のオワタツジン結果*Ver3.03
曲名:凛として咲く花の如く
曲:
譜面:No.31
コース:おわたコース(★7)
ノルマクリア成功
得点:1026720点
判定:良 573/可 0/不可 0
最大コンボ数:573回
叩けた率:100%
連打:118回
オプション:なし
譜面コード:16906247
証明コード:
#!#16906247!#1026720!#31345!#15589489!#23726650!#"""
        play_result=game.PlayResult(
            diff=3,ura=False,
            success=True,
            score=1026720,
            r0=573,r1=0,r2=0,
            maxcombo=573,lenda=118,
            option=0,
            code=16906247,
            prove="#!#16906247!#1026720!#31345!#15589489!#23726650!#",
            original=text
        )
        result=game.swf.parse("f90626fa",text)
        self.assertEqual(result,[play_result])

        text="""Hello World
*太鼓のオワタツジン結果*Ver3.03
曲名:凛として咲く花の如く
曲:
譜面:No.31
コース:おわたコース(★7)
ノルマクリア成功
得点:1026720点
判定:良 573/可 0/不可 0
最大コンボ数:573回
叩けた率:100%
連打:118回
オプション:なし
譜面コード:16906247
証明コード:
#!#16906247!#1026720!#31345!#15589489!#23726650!#"""
        result=game.swf.parse("f90626fa",text)
        self.assertEqual(result,["Hello World",play_result])

        text="""*太鼓のオワタツジン結果*Ver3.03
曲名:凛として咲く花の如く
曲:
譜面:No.31
コース:おわたコース(★7)
ノルマクリア成功
得点:1026720点
判定:良 573/可 0/不可 0
最大コンボ数:573回
叩けた率:100%
連打:118回
オプション:なし
譜面コード:16906247
証明コード:
#!#16906247!#1026720!#31345!#15589489!#23726650!#
Hello World"""
        result=game.swf.parse("f90626fa",text)
        self.assertEqual(result,[play_result,"Hello World"])

        text="""Hello A
*太鼓のオワタツジン結果*Ver3.03
曲名:凛として咲く花の如く
曲:
譜面:No.31
コース:おわたコース(★7)
ノルマクリア成功
得点:1026720点
判定:良 573/可 0/不可 0
最大コンボ数:573回
叩けた率:100%
連打:118回
オプション:なし
譜面コード:16906247
証明コード:
#!#16906247!#1026720!#31345!#15589489!#23726650!#
Hello B"""
        result=game.swf.parse("f90626fa",text)
        self.assertEqual(result,["Hello A",play_result,"Hello B"])

        text="""Hello A

*太鼓のオワタツジン結果*Ver3.03
曲名:凛として咲く花の如く
曲:
譜面:No.31
コース:おわたコース(★7)
ノルマクリア成功
得点:1026720点
判定:良 573/可 0/不可 0
最大コンボ数:573回
叩けた率:100%
連打:118回
オプション:なし
譜面コード:16906247
証明コード:
#!#16906247!#1026720!#31345!#15589489!#23726650!#

Hello B"""
        result=game.swf.parse("f90626fa",text)
        self.assertEqual(result,["Hello A",play_result,"Hello B"])

        text="""


Hello A



*太鼓のオワタツジン結果*Ver3.03
曲名:凛として咲く花の如く
曲:
譜面:No.31
コース:おわたコース(★7)
ノルマクリア成功
得点:1026720点
判定:良 573/可 0/不可 0
最大コンボ数:573回
叩けた率:100%
連打:118回
オプション:なし
譜面コード:16906247
証明コード:
#!#16906247!#1026720!#31345!#15589489!#23726650!#



Hello B


"""
        result=game.swf.parse("f90626fa",text)
        self.assertEqual(result,["Hello A",play_result,"Hello B"])

        text="""Hello A\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nHello B"""
        result=game.swf.parse("f90626fa",text)
        self.assertEqual(result,["Hello A\n\nHello B"])

        text="""Hello A\nHello B"""
        result=game.swf.parse("f90626fa",text)
        self.assertEqual(result,["Hello A\nHello B"])

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

        comment="""*太鼓のオワタツジン結果*Ver3.03
曲名:凛として咲く花の如く
曲:
譜面:No.31
コース:おわたコース(★7)
ノルマクリア成功
得点:1026720点
判定:良 573/可 0/不可 0
最大コンボ数:573回
叩けた率:100%
連打:118回
オプション:なし
譜面コード:16906247
証明コード:
#!#16906247!#1026720!#31345!#15589489!#23726650!#"""
#        pprint.pprint(comment)
#        comment=comment.encode("utf-8")
        client.post("/game/comment/", {
            "game_entry":"1",
            "comment":comment,
        })
        
        db_gamecomment=game.models.GameComment.objects.get(pk=1)
        self.assertEqual(db_gamecomment.player.username,"submitter")
        self.assertEqual(db_gamecomment.content,comment.decode("utf-8"))

        db_gamecommentcontent=game.models.GameCommentContent.objects.get(pk=1)
        self.assertEqual(db_gamecommentcontent.parent.pk,1)
        self.assertEqual(db_gamecommentcontent.part,0)
        self.assertEqual(db_gamecommentcontent.content,comment.decode("utf-8"))
        self.assertEqual(db_gamecommentcontent.is_score,True)
        
        db_scorereport=game.models.ScoreReport.objects.get(pk=1)
        self.assertEqual(db_scorereport.parent.pk,1)
        self.assertEqual(db_scorereport.diff,3)
        self.assertEqual(db_scorereport.ura,False)
        self.assertEqual(db_scorereport.success,True)
        self.assertEqual(db_scorereport.score,1026720)
        self.assertEqual(db_scorereport.r0,573)
        self.assertEqual(db_scorereport.r1,0)
        self.assertEqual(db_scorereport.r2,0)
        self.assertEqual(db_scorereport.maxcombo,573)
        self.assertEqual(db_scorereport.lenda,118)
        self.assertEqual(db_scorereport.code,16906247)
        self.assertEqual(db_scorereport.prove,"#!#16906247!#1026720!#31345!#15589489!#23726650!#")

    def test_code0_2(self):
        data_buf = open("game/test_res/data2.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,99860)

    def test_code0_3(self):
        data_buf = open("game/test_res/data3.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,99860)

    def test_code0_4(self):
        data_buf = open("game/test_res/data4.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,99865)

    def test_code0_5(self):
        data_buf = open("game/test_res/data5.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,99865)

    def test_code0_6(self):
        data_buf = open("game/test_res/data6.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,99845)

    def test_code0_7(self):
        data_buf = open("game/test_res/data7.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,99855)

    def test_code0_8(self):
        data_buf = open("game/test_res/data8.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,99970)

    def test_code0_9(self):
        data_buf = open("game/test_res/data9.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,109860)

    def test_code0_10(self):
        data_buf = open("game/test_res/data10.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,1682731)

    def test_code0_11(self):
        data_buf = open("game/test_res/data11.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,307277)

    def test_code0_12(self):
        data_buf = open("game/test_res/data12.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,1230694)

    def test_code0_13(self):
        data_buf = open("game/test_res/data13.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,1579877)

    def test_code0_14(self):
        data_buf = open("game/test_res/data14.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,85745)

    def test_code0_15(self):
        data_buf = open("game/test_res/data15.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,1687685)

    def test_code0_16(self):
        data_buf = open("game/test_res/data16.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,2450)

    def test_code0_17(self):
        data_buf = open("game/test_res/data17.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,186920)

    def test_code0_18(self):
        data_buf = open("game/test_res/data18.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,2065)

    def test_code0_19(self):
        data_buf = open("game/test_res/data19.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,2025)
        
    def test_code0_20(self):
        data_buf = open("game/test_res/data20.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,2170)

    def test_code0_21(self):
        data_buf = open("game/test_res/data21.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,2300)

    def test_code0_22(self):
        data_buf = open("game/test_res/data22.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,2155)

    def test_code0_23(self):
        data_buf = open("game/test_res/data23.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        self.assertEqual(ret,2415)

    def test_code0_x(self):
        data_buf = open("game/test_res/data.txt","r").read()
        ret = game.swf.code0._get_code(data_buf, 3)
        print ret

    def test_code1(self):
        data_buf = open("game/test_res/data.txt","r").read()
        ret = game.swf.code1._get_code(data_buf, 3)
        self.assertEqual(ret,16906677)
