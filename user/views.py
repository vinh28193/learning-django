from datetime import datetime

from django.contrib.auth import login
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from .serializers import (
    JSONWebTokenSerializer, RefreshJSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer, UserSerializer
)

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class JSONWebTokenView(GenericAPIView):
    """
    Base API View that various JWT interactions inherit from.
    """
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user, store, token = serializer.get_auth()
            login(request, user)
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration_delta = api_settings.JWT_EXPIRATION_DELTA
                expiration = datetime.utcnow() + expiration_delta
                response.set_cookie(
                    key=api_settings.JWT_AUTH_COOKIE, value=token,
                    expires=expiration, httponly=True
                )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainJSONWebToken(JSONWebTokenView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer


class VerifyJSONWebToken(JSONWebTokenView):
    """
    API View that checks the veracity of a token, returning the token if it
    is valid.
    """
    serializer_class = VerifyJSONWebTokenSerializer


class RefreshJSONWebToken(JSONWebTokenView):
    """
    API View that returns a refreshed token (with new expiration) based on
    existing token

    If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token
    """
    serializer_class = RefreshJSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()
refresh_jwt_token = RefreshJSONWebToken.as_view()
verify_jwt_token = VerifyJSONWebToken.as_view()


class UserProfileView(RetrieveAPIView):
    queryset = None
    serializer_class = UserSerializer

    def get_queryset(self):
        """Nothing for results"""

    def get_object(self):
        return self.request.user


user_profile = UserProfileView.as_view()
