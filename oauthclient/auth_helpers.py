from django.contrib.auth.models import User
from django.conf import settings
from oauth2client.client import OAuth2WebServerFlow
import urllib
import json

def check_auth(request):
    print 'authenticating'
    if 'token' in request.session:
        try:
            gmail = check_token(request.session['token'])
            if not gmail:
                print 'if not gmail'
                return False
            else:
                print 'else'
                user = User.objects.get(email=gmail) 
                
                return True
        except User.DoesNotExist:
            pass
    print 'return anon'
    return False

def check_token(token):
    uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + token
    r = urllib.urlopen(uri)
    try:
        gmail = json.loads(r.read())['emails'][0]['value']
        return gmail
    except KeyError:
        return False

def handle_redirect():
    flow = OAuth2WebServerFlow(client_id=settings.CLIENT_ID,client_secret=settings.CLIENT_SECRET, scope=settings.SCOPES,redirect_uri=settings.DEBUG_REDIRECT)
    return flow.step1_get_authorize_url()

def handle_callback(request):
    code = request.GET.get('code', '')
    flow = OAuth2WebServerFlow(client_id=settings.CLIENT_ID,client_secret=settings.CLIENT_SECRET, scope=settings.SCOPES,redirect_uri=settings.DEBUG_REDIRECT)
    credentials = flow.step2_exchange(code)
    gmail = check_token(credentials.access_token)
    try:
        user = User.objects.get(email=gmail)
    except User.DoesNotExist:
        user = User.objects.create_user(gmail, gmail, 'blank')
        user.save()
    request.session['token'] = credentials.access_token
    return gmail
        
def revoke_token(request):
    if 'token' in request.session:
        access_token = request.session['token']
        uri = 'https://accounts.google.com/o/oauth2/revoke?token=' + access_token
        urllib.urlopen(uri)
        request.session.flush()
        return None
    else:
        request.session.flush()
        return None
