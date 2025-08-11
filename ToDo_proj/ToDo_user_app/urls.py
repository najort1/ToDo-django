from django.urls import path
from . import views

app_name = 'user_app'


urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('api/users/', views.admin_users_data, name='admin_users_data'),
    path('api/gender-stats/', views.admin_gender_stats, name='admin_gender_stats'),
    path('api/age-stats/', views.admin_age_stats, name='admin_age_stats'),
    path('api/user/update-type/<int:user_id>/', views.admin_user_update_type, name='admin_user_update_type'),
    path('api/user/details/<int:user_id>/', views.admin_user_details, name='admin_user_details'),
    path('api/user/delete/<int:user_id>/', views.admin_user_delete, name='admin_user_delete'),
    path('api/user/deactivate/<int:user_id>/', views.admin_user_deactivate, name='admin_user_deactivate'),
    path('api/user/activate/<int:user_id>/', views.admin_user_activate, name='admin_user_activate'),


]
