from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('chat.urls')),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls)
]
