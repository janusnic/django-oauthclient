Quick start
-----------

1. Add "oauthclient" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'oauthclient',
    )

2. Include the oauthclient URLconf in your project urls.py like this::

    url(r'^', include('oauthclient.urls')),

3. Register a web-based Google application and enable the Google+ API.

4. Get your application credentials from the Google Developers console and place in the `settings.py` file like this::

    CLIENT_ID = '<your_client_id>'
    CLIENT_SECRET = '<your_client_secret>'
    SCOPES = 'https://www.googleapis.com/auth/userinfo.email'
    DEBUG_REDIRECT = 'localhost:8000/oauth2callback'
    PRODUCTION_REDIRECT = '<your_site>/oauth2callback'

5. Run server and visit the `/checkauth` endpoint to authenticate with Google+.
