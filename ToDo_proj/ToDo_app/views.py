from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Task
import json
from .choices import Status, Months
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.db.models import Count
from datetime import datetime, date
from django.contrib.admin.views.decorators import staff_member_required




# Funções auxiliares para reduzir duplicação de código
def handle_json_error(error_message, status_code=400):
    """Função auxiliar para retornar erros JSON padronizados"""
    return JsonResponse({'success': False, 'error': error_message}, status=status_code)


def handle_json_success(message, data=None):
    """Função auxiliar para retornar sucessos JSON padronizados"""
    response_data = {'success': True, 'message': message}
    if data:
        response_data.update(data)
    return JsonResponse(response_data)


def validate_task_data(data):
    """Função auxiliar para validar dados de tarefa"""
    title = data.get('title', '').strip()
    if not title:
        return None, 'Título é obrigatório'
    return title, None


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



@login_required
def dashboard(request):
    """
    View principal que exibe a lista de tarefas do usuário
    Inclui funcionalidade de filtro por status com paginação
    """
    # Obter parâmetro de filtro da URL
    status_filter = request.GET.get('status', '')
    
    # Buscar tarefas do usuário logado
    tasks = Task.objects.filter(user=request.user)
    
    # Aplicar filtro se fornecido (antes da paginação)
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    # Ordenar por data de criação (mais recentes primeiro)
    tasks = tasks.order_by('-created_at')
    
    # Aplicar paginação após filtro
    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Contar tarefas por status para estatísticas
    stats = {
        'total': Task.objects.filter(user=request.user).count(),
        'pending': Task.objects.filter(user=request.user, status=Status.PENDING).count(),
        'in_progress': Task.objects.filter(user=request.user, status=Status.IN_PROGRESS).count(),
        'completed': Task.objects.filter(user=request.user, status=Status.COMPLETED).count(),
    }
    
    context = {
        'stats': stats,
        'status_choices': Status.choices,
        'current_status_filter': status_filter,
        'page_obj': page_obj,
    }
    
    return render(request, 'tasks/dashboard.html', context)


@login_required
def create_task(request):
    """
    View para criar uma nova tarefa via AJAX
    """
    if request.method != 'POST':
        return handle_json_error('Método não permitido', 405)
    
    try:
        data = json.loads(request.body)
        
        # Validar dados obrigatórios
        title, error = validate_task_data(data)
        if error:
            return handle_json_error(error)
        
        # Criar nova tarefa
        task = Task.objects.create(
            user=request.user,
            title=title,
            description=data.get('description', ''),
            status=data.get('status', Status.PENDING)
        )
        
        return handle_json_success(
            'Tarefa criada com sucesso!',
            {'task': format_task_data(task)}
        )
        
    except json.JSONDecodeError:
        return handle_json_error('Dados inválidos')
    except Exception:
        return handle_json_error('Erro interno do servidor', 500)


@login_required
def update_task(request, task_id):
    """
    View para atualizar uma tarefa existente via AJAX
    """
    if request.method != 'POST':
        return handle_json_error('Método não permitido', 405)
    
    try:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        data = json.loads(request.body)
        
        # Validar título obrigatório
        title, error = validate_task_data(data)
        if error:
            return handle_json_error(error)
        
        # Atualizar campos da tarefa
        task.title = title
        task.description = data.get('description', '')
        task.status = data.get('status', task.status)
        task.save()
        
        return handle_json_success(
            'Tarefa atualizada com sucesso!',
            {'task': format_task_data(task)}
        )
        
    except Task.DoesNotExist:
        return handle_json_error('Tarefa não encontrada', 404)
    except json.JSONDecodeError:
        return handle_json_error('Dados inválidos')
    except Exception:
        return handle_json_error('Erro interno do servidor', 500)


@login_required
def delete_task(request, task_id):
    """
    View para deletar uma tarefa via AJAX
    """
    if request.method != 'DELETE':
        return handle_json_error('Método não permitido', 405)
    
    try:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task_title = task.title
        task.delete()
        
        return handle_json_success(f'Tarefa "{task_title}" removida com sucesso!')
        
    except Task.DoesNotExist:
        return handle_json_error('Tarefa não encontrada', 404)
    except Exception:
        return handle_json_error('Erro interno do servidor', 500)


@login_required
def get_task(request, task_id):
    """
    View para obter dados de uma tarefa específica via AJAX
    Usado para preencher o modal de edição
    """
    try:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        return handle_json_success('', {'task': format_task_data(task)})
        
    except Task.DoesNotExist:
        return handle_json_error('Tarefa não encontrada', 404)
    except Exception:
        return handle_json_error('Erro interno do servidor', 500)


@login_required
def complete_task(request, task_id):
    """
    View para marcar uma tarefa como concluída via AJAX
    """
    if request.method != 'POST':
        return handle_json_error('Método não permitido', 405)
    
    try:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.status = Status.COMPLETED
        task.save()
        
        return handle_json_success(f'Tarefa "{task.title}" marcada como concluída!')
        
    except Task.DoesNotExist:
        return handle_json_error('Tarefa não encontrada', 404)
    except Exception:
        return handle_json_error('Erro interno do servidor', 500)
    

@login_required
def all_tasks_date(request):
    """
    View para obter todas as datas de todas as tarefas de um usuario e separar a quantidade por mes para fins de grafico
    """
    try:
        tasks = Task.objects.filter(user=request.user)
        dates = tasks.values_list('created_at', flat=True)
        
        # Initialize counts dict with all months set to 0 (using month names as keys)
        counts = {month[1]: 0 for month in Months.choices}
        
        # Count tasks for each month
        for date in dates:
            if date:
                month = date.strftime('%m')
                month_name = dict(Months.choices)[month]
                counts[month_name] += 1
            
        return handle_json_success('', {'counts': counts})
    except Exception as e:
        return handle_json_error(f'Erro interno do servidor: {e}', 500)
