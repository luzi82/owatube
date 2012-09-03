# -*- coding: utf-8 -*-
import re

# valid
VALID_ERR =-2
VALID_FAIL=-1
VALID_PASS=1
VALID_SURE=2
# result
RESULT_FAIL=0
RESULT_PASS=1
RESULT_PERFECT=2
# score
# r0,r1,r2
# maxcombo
# lenda
# speed
# invisible
# code
# prove

parse0_re0=re.compile("""\*太鼓のオワタツジン結果\*Ver3\.03
曲名:[^\\n]*
曲:[^\\n]*
譜面:[^\\n]*
コース:[^\\n]*
ノルマクリア(?P<result>成功|失敗)
得点:(?P<score>[0-9]+)点
判定:良 (?P<r0>[0-9]+)/可 (?P<r1>[0-9]+)/不可 (?P<r2>[0-9]+)
最大コンボ数:(?P<maxcombo>[0-9]+)回
叩けた率:([0-9]+)%
連打:(?P<lenda>[0-9]+)回
オプション:(?P<option>[^\\n]+)
譜面コード:(?P<code>[0-9]+)
証明コード:
(?P<prove>#!#[0-9]+!#[0-9]+!#[0-9]+!#[0-9]+!#[0-9]+!#)""")
    
parse0_re1=re.compile("#!#(?P<code>[0-9]+)!#(?P<score>[0-9]+)!#31345!#15589489!#23726650!#")

def parse0(txt):
    m0=parse0_re0.search(txt)
    if(m0==None):return {"valid":VALID_ERR}
    m1=parse0_re1.search(m0.group("prove"))
    if(m1==None):return {"valid":VALID_ERR}
    if(m0.group("code")!=m1.group("code")):return {"valid":VALID_FAIL}
    if(m0.group("score")!=m1.group("score")):return {"valid":VALID_FAIL}
    # TODO

# func, valid-check
parser=[
    [parse0,False]
]
