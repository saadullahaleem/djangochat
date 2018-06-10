from django.contrib.auth import logout as auth_logout
from .models import Message, User
from .serializers import SocialSerializer, UserSerializer, MessageSerializer
from requests.exceptions import HTTPError
from social_django.utils import psa
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, views
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet


class LogoutView(views.APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception as e:
            pass

        auth_logout(request)

        return Response({"success": "Successfully logged out."},
                        status=status.HTTP_200_OK)


class ProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    class Meta:
        model = User
        fields = ('id', 'alias')


class MessageViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        qs = Message.objects.all().order_by('-created')
        if user_id:
            return qs.filter(user_id=user_id)
        else:
            return qs

    serializer_class = MessageSerializer


@api_view(http_method_names=['POST'])
@psa()
def exchange_token(request, backend):
    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):

        try:
            user = request.backend.do_auth(serializer.validated_data['access_token'])
        except HTTPError as e:
            return Response(
                {'errors': {
                    'auth_token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response({
                'auth_token': token.key,
                'user': {
                    'alias': user.alias,
                    'id': user.id
                }
            })
        else:
            return Response(
                {"error": "Authentication Failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
