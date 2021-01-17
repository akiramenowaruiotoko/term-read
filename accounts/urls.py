from django.urls import path
from accounts import views

urlpatterns = [
  path('login/', views.LoginViews.as_view(), name='account_login'),
  path('logout/', views.LogoutViews.as_view(), name='account_logout'),
  path('signup/', views.SignupViews.as_view(), name='account_signup'),
  
]