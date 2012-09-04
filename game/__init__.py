import inspect

RESULT_FAIL=-1
RESULT_PASS=1
RESULT_PERFECT=2

class PlayResult:
    
    def __init__(self,result,score,r0,r1,r2,maxcombo,lenda,option,code):
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        for arg in args:
            setattr(self,arg,values[arg])
