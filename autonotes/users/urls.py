from django.urls import path

from .views import UserCreateView, UserCurrentView, UserUpdatePasswordView

urlpatterns = [
    path('', UserCreateView.as_view()),
    path('current/', UserCurrentView.as_view()),
    path('update-password/', UserUpdatePasswordView.as_view()),
]
