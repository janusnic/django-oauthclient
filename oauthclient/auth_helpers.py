import requests
from django.contrib.auth.models import User
from django.conf import settings
from oauth2client.client import OAuth2WebServerFlow

def check_token(token):
    headers = {"accept-encoding": "gzip, deflate", "accept": "application/json", "user-agent": "google-api-python-client/1.0"}
    uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + token
    r = requests.get(uri, headers=headers)
    if r.status_code == 401:
        return False
    try:
        gmail = r.json()['emails'][0]['value']
        return gmail
    except KeyError:
        return False

def handle_redirect():
    flow = OAuth2WebServerFlow(client_id=settings.CLIENT_ID,client_secret=settings.CLIENT_SECRET, scope=settings.SCOPES,redirect_uri=settings.DEBUG_REDIRECT)
    return flow.step1_get_authorize_url()

def handle_callback(request):
    code = request.query_params['code']
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
        headers = {"accept-encoding": "gzip, deflate", "accept": "application/json", "user-agent": "google-api-python-client/1.0"}
        uri = 'https://accounts.google.com/o/oauth2/revoke?token=' + access_token
        r = requests.get(uri, headers=headers)
        request.session.flush()
        return r
    else:
        request.session.flush()
        return None
