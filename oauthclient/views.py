from django.shortcuts import redirect
from django.http import HttpResponse
from auth_helpers import *

# Required views for Google+ authentication   
def revoke(request):
    r = revoke_token(request)
    return HttpResponse('token revoked')

def oauth2_callback(request):
    result = handle_callback(request)
    return redirect('/checkauth')



def checkauth(request):
    if check_auth(request):
        # User has been authenticated, form response here.
        return HttpResponse('authenticated')
    else:
        # Required redirect
        return redirect(handle_redirect())
    



    
    
    
