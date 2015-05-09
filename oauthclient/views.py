from oauthclient.auth import GoogleOAuth
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from rest_framework.views import APIView
import requests
from auth_helpers import *

# Required views for Google+ authentication   
@api_view()
def revoke(request):
    r = revoke_token(request)
    return Response({"message": "token revoked"})

@api_view()
def oauth2_callback(request):
    result = handle_callback(request)
    return redirect('/checkauth')

# Model views follow this general layout
class CustomModelView(APIView):
    authentication_classes = (GoogleOAuth,)
    serializer_class = None
    def get(self, request):
        if request.user.is_authenticated():
            # User has been authenticated, form response here.
            return Response({"message": "authenticated"})
        else:
            # Required redirect
            return redirect(handle_redirect())



    
    
    
