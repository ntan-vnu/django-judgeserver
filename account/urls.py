from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.urls import path

from account.views import UserLoginView, UserPasswordChangeView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
