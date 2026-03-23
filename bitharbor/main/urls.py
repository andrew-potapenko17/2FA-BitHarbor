from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_action, name='logout'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('verify_mail/', views.verify_mail, name='verify_mail'),
    path('disable_2fa/', views.disable_2fa, name='disable_2fa'),
]
