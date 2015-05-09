from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from oauthclient import views

urlpatterns = [
    url(r'^checkauth/$', views.CustomModelView.as_view()),
    url(r'^revoke/$',views.revoke, name='revoke'),
    url(r'^oauth2callback', views.oauth2_callback, name='oauth2callback')
]

urlpatterns = format_suffix_patterns(urlpatterns)
