from django.urls import path

from user.views import (
    obtain_jwt_token, verify_jwt_token, refresh_jwt_token, user_profile
)

urlpatterns = [
    path('jwt-token/obtain/', obtain_jwt_token),
    path('jwt-token/verify/', verify_jwt_token),
    path('jwt-token/refresh/', refresh_jwt_token),
    path('profile/', user_profile),
]
