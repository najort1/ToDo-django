from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/step2/', views.register_step2, name='register_step2'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/', views.delete_account, name='delete'),
]
