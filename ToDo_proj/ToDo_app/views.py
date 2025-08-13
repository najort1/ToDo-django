from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Task
import json
from .choices import Status, Months
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.db.models import Count, Q

from datetime import datetime, date
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import DeleteView, ListView, CreateView, UpdateView,DetailView
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TaskForm
from .mixins import JsonResponseMixin



def format_task_data(task):
    """Função auxiliar para formatar dados de tarefa para JSON"""
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'created_at': task.created_at.strftime('%d/%m/%Y %H:%M'),
        'updated_at': task.updated_at.strftime('%d/%m/%Y %H:%M')
    }


# Create your views here.
def index(request):
    return render(request, 'index.html')

#de 39 pra 28 linhas
class DashboardView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/dashboard.html'
    context_object_name = 'tasks'
    paginate_by = 5
    ordering = '-created_at'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        status_filter = self.request.GET.get('status', '')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_filter = self.request.GET.get('status', '') #pegar filtro de status
        stats_query = (
            Task.objects
            .filter(user=self.request.user)
            .aggregate(
                total=Count('id'),
                pending=Count('id', filter=Q(status=Status.PENDING)),
                in_progress=Count('id', filter=Q(status=Status.IN_PROGRESS)),
                completed=Count('id', filter=Q(status=Status.COMPLETED)),
            )
        )
        
        context['status_choices'] = Status.choices
        context['current_status_filter'] = status_filter
        context['stats'] = stats_query
        
        return context
    
    
#de 32 pra 32 linhas
class CreateTaskView(LoginRequiredMixin, CreateView,JsonResponseMixin):
    model = Task
    form_class = TaskForm

    def post(self, request, *args, **kwargs):
        try:
            data = self.validate_json_request(request)
            form = self.form_class(data)
            
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return self.json_success('Tarefa criada com sucesso!',{'task': format_task_data(task)})
            else:
                return self.json_error(form.errors.as_json())


                
        except json.JSONDecodeError:
            return self.json_error('Formato JSON inválido', 400)
        except Exception as e:
            return self.json_error(f'Erro interno do servidor: {str(e)}', 500)
        

#de 32 pra 25 linhas
class UpdateTaskView(LoginRequiredMixin, UpdateView,JsonResponseMixin):
    model = Task
    form_class = TaskForm

    def post(self, request, *args, **kwargs):
        try:
            task = self.get_object()
            data = self.validate_json_request(request)
            form = self.form_class(data, instance=task)

            if form.is_valid():
                form.save()
                return self.json_success(
                    'Tarefa atualizada com sucesso!',
                    {'task': format_task_data(task)}
                )
            else:
                return self.json_error(form.errors.as_json())

        except json.JSONDecodeError:
            return self.json_error('Formato JSON inválido', 400)
        except Exception as e:
            return self.json_error(f'Erro interno do servidor: {str(e)}', 500)

    def get_object(self, queryset=None):
        return get_object_or_404(Task, id=self.kwargs['pk'], user=self.request.user)


#de 18 pra 15 linhas
class TaskDeleteView(LoginRequiredMixin, DeleteView,JsonResponseMixin):

    model = Task

    def delete(self, request, *args, **kwargs):
        try:
            task = self.get_object()
            task_title = task.title
            task.delete()
            return self.json_success(f'Tarefa "{task_title}" removida com sucesso!')

        except Task.DoesNotExist:
            return self.json_error('Tarefa não encontrada', 404)
        except Exception as e:
            return self.json_error(f'Erro interno do servidor: {str(e)}', 500)

    def get_object(self, queryset=None):
        return get_object_or_404(Task, id=self.kwargs['pk'], user=self.request.user)



class TaskDetailView(LoginRequiredMixin, DetailView,JsonResponseMixin):
    model = Task
    def get(self, request, *args, **kwargs):
        task = self.get_object()
        return self.json_success('', {'task': format_task_data(task)})
    
    def get_object(self, queryset=None):
        return get_object_or_404(Task, id=self.kwargs['pk'], user=self.request.user)


#apartir daqui eu cansei de contar a contagem de linhas so irei continuar refatorando

class TaskCompleteView(LoginRequiredMixin,View,JsonResponseMixin):

    model = Task
    fields = ['status']

    def post(self, request, *args, **kwargs):
        try:
            task = self.get_object()
            task.status = Status.COMPLETED
            task.save()
            return self.json_success(f'Tarefa "{task.title}" marcada como concluída!')

        except Task.DoesNotExist:
            return self.json_error('Tarefa não encontrada', 404)
        except Exception as e:
            return self.json_error(f'Erro interno do servidor: {e}', 500)

        
    def get_object(self, queryset=None):
        return get_object_or_404(Task, id=self.kwargs['pk'], user=self.request.user)



class AllTasksDateView(LoginRequiredMixin, View,JsonResponseMixin):

    def get(self, request, *args, **kwargs):
        try:
            tasks = Task.objects.filter(user=request.user)
            dates = tasks.values_list('created_at', flat=True)
            
            counts = {month[1]: 0 for month in Months.choices}
            
            for dt in dates:
                if dt:
                    month = dt.strftime('%m')
                    month_name = dict(Months.choices)[month]
                    counts[month_name] += 1
            
            return self.json_success('', {'counts': counts})

        except Exception as e:
            return self.json_error(f'Erro interno do servidor: {e}', 500)
