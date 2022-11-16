from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy


class UserLoginView(LoginView):
    template_name = 'admin/login.html'


class UserPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('account:logout')
