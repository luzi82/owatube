# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import re
import game.swf
import game
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
        m=game.swf.parse0_re0.search(text)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("result"),"成功")
        self.assertEqual(m.group("score"),"1026720")
        self.assertEqual(m.group("r0"),"573")
        self.assertEqual(m.group("r1"),"0")
        self.assertEqual(m.group("r2"),"0")
        self.assertEqual(m.group("maxcombo"),"573")
        self.assertEqual(m.group("lenda"),"118")
        self.assertEqual(m.group("option"),"なし")
        self.assertEqual(m.group("code"),"16906247")
        self.assertEqual(m.group("prove"),"#!#16906247!#1026720!#31345!#15589489!#23726650!#")
        
        m2=game.swf.parse0_re1.search(m.group("prove"))
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
            diff=4,ura=False,
            result=True,
            score=1026720,
            r0=573,r1=0,r2=0,
            maxcombo=573,lenda=118,
            option=0,
            code=16906247,
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
        
        data_f=open("game/test_res/data.txt")
        bgm_f=open("game/test_res/bgm.mp3")
        response = client.post("/game/upload/", {
            "data":data_f,
            "bgm":bgm_f,
            "swf":"f90626fa",
        })
        self.assertRedirects(response,"/g/1/")
