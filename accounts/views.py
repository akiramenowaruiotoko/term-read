from django.shortcuts import render, redirect
from allauth.account import views


class LoginViews(views.LoginView):
  template_name = 'accounts/login.html'


class LogoutViews(views.LogoutView):
  template_name = 'accounts/logout.html'

  def post(self, *args, **kwargs):
    if self.request.user.is_authenticated:
      self.logout()
    return redirect('/')


class SignupViews(views.SignupView):
  template_name = 'accounts/signup.html'