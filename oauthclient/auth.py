from django.contrib.auth.models import User, AnonymousUser
from rest_framework import authentication
from auth_helpers import check_token

class GoogleOAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        if 'token' in request.session:
            try:
                gmail = check_token(request.session['token'])
                if not gmail:
                    return (AnonymousUser(), None)
                else:
                    user = User.objects.get(email=gmail) 
                    return (user,None)
            except User.DoesNotExist:
                pass
        return (AnonymousUser(), None)




