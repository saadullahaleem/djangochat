from django.conf.urls import url, include
from .views import exchange_token, ProfileView, MessageViewSet, LogoutView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'messages', MessageViewSet, base_name='messages')

urlpatterns = [
    url(r'^oauth/(?P<backend>[^/]+)/$', exchange_token),
    url(r'^', include(router.urls)),
    url(r'^auth/logout/$', LogoutView.as_view()),
    url(r'^profile/$', ProfileView.as_view())
]
