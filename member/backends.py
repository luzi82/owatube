from member import owtforum
from django.contrib.auth.models import User

class OwtForumBackend:
    
    def authenticate(self, username=None, password=None):
        if owtforum.check_password(username, password) == -1:
            return None
        
        try:
            user = User.objects.get(username__exact = username)
        except User.DoesNotExist:
            user = User(username = username)
            user.is_staff = False
            user.is_superuser = False
            user.set_unusable_password()
            user.save()

        return user

    def get_user(self, user_id):
        user = User.objects.get(pk = user_id)
        return user
