from django.urls import path

from user.views import (
    UserProfileView, LoginView
)

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('profile/', UserProfileView.as_view()),
]
