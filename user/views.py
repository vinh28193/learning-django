from datetime import datetime

from django.contrib.auth import login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .serializers import UserSerializer, LoginSerializer

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class UserProfileView(RetrieveAPIView):
    queryset = None
    serializer_class = UserSerializer

    def get_queryset(self):
        """Nothing for results"""

    def get_object(self):
        return self.request.user


class LoginView(GenericAPIView):
    queryset = None
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.get_user() or request.user
            login(request, user)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (
                        datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
                )
                response.set_cookie(
                    key=api_settings.JWT_AUTH_COOKIE,
                    value=token,
                    expires=expiration,
                    httponly=True
                )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
