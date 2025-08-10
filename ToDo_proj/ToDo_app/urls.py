from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # APIs para operações CRUD das tarefas
    path('create/', views.create_task, name='create_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('get/<int:task_id>/', views.get_task, name='get_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    
    path('all_dates/', views.all_tasks_date, name='tasks_by_month'),


]
