import inspect
import pprint

class PlayResult:
    
    def __init__(self,diff,ura,result,score,r0,r1,r2,maxcombo,lenda,option,code,original):
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        for arg in args:
            setattr(self,arg,values[arg])

    def __eq__(self,other):
        if self is other:return True
        if other.__class__!=PlayResult:return False
        dir_self=dir(self)
        dir_other=dir(other)
        if dir_self!=dir_other:return False
        for a in dir_self:
            if(a.startswith("__")):continue
            if(a=="self"):continue
            self_a=getattr(self,a)
            other_a=getattr(other,a)
            if self_a!=other_a:return False
        return True
