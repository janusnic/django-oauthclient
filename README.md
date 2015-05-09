## Installation
1. Add "oauthclient" to your INSTALLED_APPS setting.
```
INSTALLED_APPS = (
    ...
    'oauthclient',
)
```
2. Include the oauthclient URLconf in your project urls.py.
```
url(r'^', include('oauthclient.urls')),
```
3. Register a web-based Google application and enable the Google+ API.
4. Get your application credentials from the Google Developers console and place in the following in your `settings.py` file.
```
CLIENT_ID = '<your_client_id>'
CLIENT_SECRET = '<your_client_secret>'
SCOPES = 'https://www.googleapis.com/auth/userinfo.email'
CALLBACK_URI = 'http://127.0.0.1:8000/oauth2callback'
REDIRECT_URI  = '/login'
```
5. Run server and visit the `/login` endpoint to authenticate with Google+.

## Authentication Flow
1. The login process begins by redirecting a user to the Google login url provided by the included `handle_redirect()` function.
2. Once the user provides their credentials, an authorization code is sent to the `/oauth2callback` endpoint which is already provided by the `oauthclient` app.
3. This code is exchanged for an access token which is then stored in Django's session under `request.session['token']`.
4. Subsequent calls to the Google+ API, such as getting user information, can use that stored access token.

## Public functions (included with oauthclient.auth_helpers)
- `me(request)` - Return JSON representation of the Google user. Will return a "Not Authenticated" message if the user has not yet logged in. Requires a Django HttpRequest object to read the token stored in `request.session`.
- `check_auth(request)` - Returns `True` if the user has signed in with Google, `False` otherwise. Requires a Django HttpRequest object to read the token stored in `request.session`.
- `handle_redirect()` - Provides a login url using the credentials configured in `settings.py` (Step 4 above).

## Endpoints (included with oauthclient.urls)
- `/login` - Sends the user to the Google sign on page if they have not yet authenticated. Returns the user as JSON otherwise.
- `/revoke` - Revoke the current access token and log the user out.
- `/oauth2callback` - Used by `oauthclient` to receive an authorization code from Google and store the access token. This endpoint should not be overwritten as it is required to perform the authentication.

## Example Usage
```
from django.http import JsonResponse
# Required imports
from django.shortcuts import redirect
from oauthclient.auth_helpers import *

# Function-based view that displays the Google+ user as JSON once authenticated.
def my_view(request):
    if check_auth(request):
        # User has been authenticated, form response here.
        return JsonResponse(me(request))
    else:
        # Required redirect
        return redirect(handle_redirect())
```
