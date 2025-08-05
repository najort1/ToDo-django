from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Task
import json


# Create your views here.]
def index(request):
    return render(request, 'index.html')



@login_required
def dashboard(request):
    """
    View principal que exibe a lista de tarefas do usuário
    Inclui funcionalidade de filtro simples por status
    """
    # Obter parâmetro de filtro da URL
    status_filter = request.GET.get('status', '')
    
    # Buscar tarefas do usuário logado
    tasks = Task.objects.filter(user=request.user)
    
    # Aplicar filtro se fornecido
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    # Ordenar por data de criação (mais recentes primeiro)
    tasks = tasks.order_by('-created_at')
    
    # Contar tarefas por status para estatísticas
    stats = {
        'total': Task.objects.filter(user=request.user).count(),
        'pending': Task.objects.filter(user=request.user, status=Task.Status.PENDING).count(),
        'in_progress': Task.objects.filter(user=request.user, status=Task.Status.IN_PROGRESS).count(),
        'completed': Task.objects.filter(user=request.user, status=Task.Status.COMPLETED).count(),
    }
    
    context = {
        'tasks': tasks,
        'stats': stats,
        'status_choices': Task.Status.choices,
        'current_status_filter': status_filter,
    }
    
    return render(request, 'tasks/dashboard.html', context)


@login_required
def create_task(request):
    """
    View para criar uma nova tarefa via AJAX
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validar dados obrigatórios
            title = data.get('title', '').strip()
            if not title:
                return JsonResponse({
                    'success': False, 
                    'error': 'Título é obrigatório'
                }, status=400)
            
            # Criar nova tarefa
            task = Task.objects.create(
                user=request.user,
                title=title,
                description=data.get('description', ''),
                status=data.get('status', Task.Status.PENDING)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Tarefa criada com sucesso!',
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'status': task.status,
                    'created_at': task.created_at.strftime('%d/%m/%Y %H:%M')
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False, 
                'error': 'Dados inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': 'Erro interno do servidor'
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)


@login_required
def update_task(request, task_id):
    """
    View para atualizar uma tarefa existente via AJAX
    """
    if request.method == 'POST':
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            data = json.loads(request.body)
            
            # Validar título obrigatório
            title = data.get('title', '').strip()
            if not title:
                return JsonResponse({
                    'success': False, 
                    'error': 'Título é obrigatório'
                }, status=400)
            
            # Atualizar campos da tarefa
            task.title = title
            task.description = data.get('description', '')
            task.status = data.get('status', task.status)
            task.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Tarefa atualizada com sucesso!',
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'status': task.status,
                    'updated_at': task.updated_at.strftime('%d/%m/%Y %H:%M')
                }
            })
            
        except Task.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': 'Tarefa não encontrada'
            }, status=404)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False, 
                'error': 'Dados inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': 'Erro interno do servidor'
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)


@login_required
def delete_task(request, task_id):
    """
    View para deletar uma tarefa via AJAX
    """
    if request.method == 'DELETE':
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            task_title = task.title
            task.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Tarefa "{task_title}" removida com sucesso!'
            })
            
        except Task.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': 'Tarefa não encontrada'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': 'Erro interno do servidor'
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)


@login_required
def get_task(request, task_id):
    """
    View para obter dados de uma tarefa específica via AJAX
    Usado para preencher o modal de edição
    """
    try:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        
        return JsonResponse({
            'success': True,
            'task': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'created_at': task.created_at.strftime('%d/%m/%Y %H:%M'),
                'updated_at': task.updated_at.strftime('%d/%m/%Y %H:%M')
            }
        })
        
    except Task.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'error': 'Tarefa não encontrada'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': 'Erro interno do servidor'
        }, status=500)


@login_required
def complete_task(request, task_id):
    """
    View para marcar uma tarefa como concluída via AJAX
    """
    if request.method == 'POST':
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            
            # Marcar como concluída
            task.status = Task.Status.COMPLETED
            task.completed = True
            task.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Tarefa "{task.title}" marcada como concluída!'
            })
            
        except Task.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': 'Tarefa não encontrada'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': 'Erro interno do servidor'
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)