from member import owtforum
from django.contrib.auth.models import User

class OwtForumBackend:
    
    def authenticate(self, username=None, password=None):
        if owtforum.check_password(username, password) == -1:
            return None
        
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            user = User(username = username, password = "")
            user.is_staff = False
            user.is_superuser = False
            user.save()

        return user

    def get_user(self, user_id):
        user = User.objects.get(pk = user_id)
        return user
