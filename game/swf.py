# -*- coding: utf-8 -*-
import re
import inspect
import game
import pprint

# valid
# result
# score
# r0,r1,r2
# maxcombo
# lenda
# speed
# invisible
# code
# prove

DIFF_MAP={
    "かんたん":1,
    "ふつう":2,
    "むずかしい":3,
    "おわた":4,
}

class BadProve(Exception):
    pass

parse0_re0=re.compile("""(\*太鼓のオワタツジン結果\*Ver3\.03
曲名:(?P<title>[^\\n]*)
曲:[^\\n]*
譜面:[^\\n]*
コース:(?P<diff>(かんたん)|(ふつう)|(むずかしい)|(おわた))[^\\n]*
ノルマクリア(?P<result>(成功)|(失敗))
得点:(?P<score>[0-9]+)点
判定:良 (?P<r0>[0-9]+)/可 (?P<r1>[0-9]+)/不可 (?P<r2>[0-9]+)
最大コンボ数:(?P<maxcombo>[0-9]+)回
叩けた率:([0-9]+)%
連打:(?P<lenda>[0-9]+)回
オプション:(?P<option>[^\\n]+)
譜面コード:(?P<code>[0-9]+)
証明コード:
(?P<prove>#!#[0-9]+!#[0-9]+!#[0-9]+!#[0-9]+!#[0-9]+!#))""")
    
parse0_re1=re.compile("#!#(?P<code>[0-9]+)!#(?P<score>[0-9]+)!#31345!#15589489!#23726650!#")

def parse0(txt):
    buf=txt
    a1=[]
    
    while len(buf)!=0:
        m0=parse0_re0.search(buf)
        if(m0==None):
            a1.append(buf)
            break
        a1.append(buf[0:m0.start()])
        m1=parse0_re1.search(m0.group("prove"))
        if(m0.group("code")!=m1.group("code")):raise BadProve()
        if(m0.group("score")!=m1.group("score")):raise BadProve()
        a1.append(game.PlayResult(
            diff=DIFF_MAP[m0.group("diff")],
            ura=m0.group("title").endswith("(裏)"),
            result=(m0.group("result")=="成功"),
            score=int(m0.group("score")),
            r0=int(m0.group("r0")),
            r1=int(m0.group("r1")),
            r2=int(m0.group("r2")),
            maxcombo=int(m0.group("maxcombo")),
            lenda=int(m0.group("lenda")),
            option=0,
            code=int(m0.group("code")),
            original=m0.group()
        ))
        buf=buf[m0.end():]

    a0=a1
    a1=[]
    for x in a0:
        if isinstance(x,game.PlayResult):
            a1.append(x)
            continue
        y=x
        y=re.sub("^\s+$","",y,flags=re.MULTILINE)
        y=re.sub("^\n","",y)
        y=re.sub("\n$","",y)
        if len(y)!=0:
            a1.append(y)
    
    return a1
    
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

def parse(key,txt):
    return SWF_LIST[key].parser(txt)
