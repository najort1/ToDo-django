from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('register/', views.AuthRegisterView.as_view(), name='register'),
    path('register/step2/', views.AuthRegisterStep2.as_view(), name='register_step2'),
    path('login/', views.AuthLoginView.as_view(), name='login'),

    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('delete/', views.DeleteAccountView.as_view(), name='delete'),
]
