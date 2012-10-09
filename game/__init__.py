import inspect
import pprint
import models

class PlayResult:
    
    # diff: int
    # ura: bool
    # success: bool
    # score: int
    # r0,r1,r2: int
    # maxcombo: int
    # lenda: int
    # option: int # change later
    # code: int
    # prove: str
    # original: str
    def __init__(self,diff,ura,success,score,r0,r1,r2,maxcombo,lenda,option,code,prove,original):
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

def create_empty_star_list():
    return [ [ 0 for i in xrange(4) ] for i in xrange(2) ]


def get_game_star(db_game):
    ret = create_empty_star_list()
    db_diff_list = models.GameDiff.objects.filter(game = db_game)
    for db_diff in db_diff_list:
        x = 1 if db_diff.ura else 0
        y = db_diff.diff
        v = db_diff.star
        ret[x][y] = v
    return ret
