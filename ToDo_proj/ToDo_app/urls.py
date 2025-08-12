from django.urls import path
from . import views


app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    
    # APIs para operações CRUD das tarefas
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path('update/<int:pk>/', views.UpdateTaskView.as_view(), name='update_task'),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name='delete_task'),
    path('get/<int:pk>/', views.TaskDetailView.as_view(), name='get_task'),
    path('complete/<int:pk>/', views.TaskCompleteView.as_view(), name='complete_task'), 
    path('all_dates/', views.AllTasksDateView.as_view(), name='tasks_by_month'),



]
