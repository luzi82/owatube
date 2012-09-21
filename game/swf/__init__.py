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
    def __init__(self,swf_id,name,enabled,data_parser):
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        for arg in args:
            setattr(self,arg,values[arg])

SWF_LIST={}

def _reg_swf(*args):
    SWF_LIST[args[0]]=Swf(*args)

## swf reg START
_reg_swf("f90626fa","3.03. A",True,parse_data_0)
## swf reg END

SWF_CHOICE=[]
for k,swf in SWF_LIST.iteritems():
    if(swf.enabled==False):continue
    t=(k,swf.name)
    SWF_CHOICE.append(t)
#SWF_CHOICE=[(swf.swf_id,swf.name)for swf in SWF_LIST]
#SWF_CHOICE=[("f90626fa","3.03. A")]

def parse_data(key,buf):
    return SWF_LIST[key].data_parser(buf)
