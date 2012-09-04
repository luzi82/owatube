# -*- coding: utf-8 -*-
import re
import inspect

# valid
VALID_ERR =-2
VALID_FAIL=-1
VALID_PASS=1
# result
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
    
class Swf:
    def __init__(self,swf_id,name,enabled,parser):
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        for arg in args:
            setattr(self,arg,values[arg])

SWF_LIST={}

def _reg_swf(*args):
    SWF_LIST[args[0]]=Swf(*args)

## swf reg START
_reg_swf("f90626fa","3.03. A",True,parse0)
## swf reg END

SWF_CHOICE=[]
for k,swf in SWF_LIST.iteritems():
    if(swf.enabled==False):continue
    t=(k,swf.name)
    SWF_CHOICE.append(t)
#SWF_CHOICE=[(swf.swf_id,swf.name)for swf in SWF_LIST]
#SWF_CHOICE=[("f90626fa","3.03. A")]
