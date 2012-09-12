# -*- coding: utf-8 -*-
import re
import inspect
import game
import pprint
import chardet

# valid
# success
# score
# r0,r1,r2
# maxcombo
# lenda
# speed
# invisible
# code
# prove

# start from 0, since of array index
DIFF_MAP={
    "かんたん":0,
    "ふつう":1,
    "むずかしい":2,
    "おわた":3,
}

class BadProve(Exception):
    pass

parse_report_0_re0=re.compile("""(\*太鼓のオワタツジン結果\*Ver3\.03(\\r)?
曲名:(?P<title>[^\\r\\n]*)(\\r)?
曲:[^\\r\\n]*(\\r)?
譜面:[^\\r\\n]*(\\r)?
コース:(?P<diff>(かんたん)|(ふつう)|(むずかしい)|(おわた))[^\\r\\n]*(\\r)?
ノルマクリア(?P<success>(成功)|(失敗))(\\r)?
得点:(?P<score>[0-9]+)点(\\r)?
判定:良 (?P<r0>[0-9]+)/可 (?P<r1>[0-9]+)/不可 (?P<r2>[0-9]+)(\\r)?
最大コンボ数:(?P<maxcombo>[0-9]+)回(\\r)?
叩けた率:([0-9]+)%(\\r)?
連打:(?P<lenda>[0-9]+)回(\\r)?
オプション:(?P<option>[^\\r\\n]+)(\\r)?
譜面コード:(?P<code>[0-9]+)(\\r)?
証明コード:(\\r)?
(?P<prove>#!#[0-9]+!#[0-9]+!#[0-9]+!#[0-9]+!#[0-9]+!#))""")
    
parse_report_0_re1=re.compile("#!#(?P<code>[0-9]+)!#(?P<score>[0-9]+)!#31345!#15589489!#23726650!#")

def parse_report_0(txt):
    buf=txt
    a1=[]
    
    while len(buf)!=0:
        m0=parse_report_0_re0.search(buf)
        if(m0==None):
            a1.append(buf)
            break
        a1.append(buf[0:m0.start()])
        m1=parse_report_0_re1.search(m0.group("prove"))
        if(m0.group("code")!=m1.group("code")):raise BadProve()
        if(m0.group("score")!=m1.group("score")):raise BadProve()
        a1.append(game.PlayResult(
            diff=DIFF_MAP[m0.group("diff")],
            ura=m0.group("title").endswith("(裏)"),
            success=(m0.group("success")=="成功"),
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

# title, music_by, data_by, diff[]
def parse_data_0(buf):
#    f=open(filename)
#    buf=f.read()
    encoding=chardet.detect(buf)["encoding"]
    content=buf.decode(encoding).encode("utf-8")
    
    ret={
        "title":None,
        "music_by":None,
        "data_by":None,
        "diff":[0,0,0,0],
    }
    m=re.search("^&title=(.*)$",content,flags=re.MULTILINE)
    if m != None:ret["title"]=m.group(1).strip()
    m=re.search("^&music_by=(.*)$",content,flags=re.MULTILINE)
    if m != None:ret["music_by"]=m.group(1).strip()
    m=re.search("^&data_by=(.*)$",content,flags=re.MULTILINE)
    if m != None:ret["data_by"]=m.group(1).strip()
    m=re.search("^&level1=(.*)$",content,flags=re.MULTILINE)
    if m != None:ret["diff"][0]=int(m.group(1).strip())
    m=re.search("^&level2=(.*)$",content,flags=re.MULTILINE)
    if m != None:ret["diff"][1]=int(m.group(1).strip())
    m=re.search("^&level3=(.*)$",content,flags=re.MULTILINE)
    if m != None:ret["diff"][2]=int(m.group(1).strip())
    m=re.search("^&level4=(.*)$",content,flags=re.MULTILINE)
    if m != None:ret["diff"][3]=int(m.group(1).strip())
    return ret

class Swf:
    def __init__(self,swf_id,name,enabled,report_parser,data_parser):
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        for arg in args:
            setattr(self,arg,values[arg])

SWF_LIST={}

def _reg_swf(*args):
    SWF_LIST[args[0]]=Swf(*args)

## swf reg START
_reg_swf("f90626fa","3.03. A",True,parse_report_0,parse_data_0)
## swf reg END

SWF_CHOICE=[]
for k,swf in SWF_LIST.iteritems():
    if(swf.enabled==False):continue
    t=(k,swf.name)
    SWF_CHOICE.append(t)
#SWF_CHOICE=[(swf.swf_id,swf.name)for swf in SWF_LIST]
#SWF_CHOICE=[("f90626fa","3.03. A")]

def parse(key,txt):
    return SWF_LIST[key].report_parser(txt)

def parse_data(key,buf):
    return SWF_LIST[key].data_parser(buf)
