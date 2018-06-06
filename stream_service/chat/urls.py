from django.conf.urls import url
from .views import home, update_profile, logout, get_all_messages


urlpatterns = [
    url(r'^$', home),
    url(r'^profile/$', update_profile),
    url(r'^auth/logout/$', logout),
    url(r'^messages/(?P<user_alias>[^/]+)/$', get_all_messages)
]
