from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Count
from datetime import date
import json
from ToDo_app.models import Task
from .models import Address
from django.views.generic import DeleteView, ListView, CreateView, UpdateView,DetailView
from django.views import View
from ToDo_app.mixins import JsonResponseMixin


# Create your views here.
User = get_user_model()
    



@staff_member_required
def admin_user_update_type(request, user_id):
    """
    API para atualizar apenas o tipo de usuário
    """
    if request.method != 'POST':
        return handle_json_error('Método não permitido', 405)
    
    try:
        user = get_object_or_404(User, id=user_id)
        data = json.loads(request.body)
        
        # Atualizar apenas o tipo de usuário
        if data.get('user_type'):
            user.user_type = data['user_type']
            if data['user_type'] == 'A':
                user.is_staff = True
            elif data['user_type'] == 'O':
                user.is_staff = False

            user.save()
            
            type_display = dict([('A', 'Admin'), ('U', 'Usuário'), ('O', 'Observer')]).get(data['user_type'], 'Usuário')
            return handle_json_success(f'Tipo de usuário alterado para {type_display} com sucesso!')
        else:
            return handle_json_error('Tipo de usuário não informado')
        
    except User.DoesNotExist:
        return handle_json_error('Usuário não encontrado', 404)
    except json.JSONDecodeError:
        return handle_json_error('Dados inválidos')
    except Exception as e:
        return handle_json_error(f'Erro interno: {str(e)}', 500)


@staff_member_required
def admin_user_details(request, user_id):
    """
    API para obter detalhes completos do usuário incluindo endereço e estatísticas de tasks
    """
    try:
        
        user = get_object_or_404(User, id=user_id)
        
        user_data = {
            'id': user.id,
            'full_name': f"{user.first_name if user.first_name else '?'} {user.last_name if user.last_name else '?'}".strip(),
            'email': user.email,
            'cpf': user.cpf or 'Não informado',
            'phone': user.phone or 'Não informado',
            'birthdate': user.birthdate.strftime('%d/%m/%Y') if user.birthdate else 'Não informado',
            'age': None,
            'gender_display': dict([('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')]).get(user.gender, 'Não informado'),
            'user_type_display': dict([('A', 'Admin'), ('U', 'Usuário'), ('O', 'Observer')]).get(user.user_type, 'Usuário'),
            'is_active': 'Ativo' if user.is_active else 'Inativo',
            'date_joined': user.date_joined.strftime('%d/%m/%Y às %H:%M') if user.date_joined else 'Não informado',
            'profile_completed': 'Sim' if user.profile_completed else 'Não'
        }
        
        # Calcular idade se birthdate existir
        if user.birthdate:
            today = date.today()
            age = today.year - user.birthdate.year - ((today.month, today.day) < (user.birthdate.month, user.birthdate.day))
            user_data['age'] = f"{age} anos"
        else:
            user_data['age'] = 'Não informado'
        
        # Dados do endereço
        address_data = {
            'formatted_address': 'Não informado',
            'zipcode': 'Não informado',
            'city_state': 'Não informado'
        }
        
        try:
            address = Address.objects.get(user=user)
            address_data = {
                'formatted_address': address.formatted_address or 'Não informado',
                'zipcode': address.zipcode or 'Não informado',
                'city_state': f"{address.city}/{address.state}" if address.city and address.state else 'Não informado'
            }
        except Address.DoesNotExist:
            pass
        
        # Estatísticas de tasks
        tasks = Task.objects.filter(user=user)
        task_stats = {
            'total': tasks.count(),
            'pending': tasks.filter(status='PENDENTE').count(),
            'in_progress': tasks.filter(status='EM ANDAMENTO').count(),
            'completed': tasks.filter(status='COMPLETADO').count()
        }
        
        return JsonResponse({
            'user': user_data,
            'address': address_data,
            'task_stats': task_stats
        })
        
    except User.DoesNotExist:
        return handle_json_error('Usuário não encontrado', 404)
    except Exception as e:
        return handle_json_error(f'Erro interno: {str(e)}', 500)


@staff_member_required
def admin_dashboard(request):
    if request.user.user_type == 'A' or request.user.is_staff or request.user.user_type == 'O':
        return render(request, 'admin_dashboard.html')
    else:
        return render(request, 'tasks/dashboard.html')



@staff_member_required
def admin_users_data(request):
    """
    API para obter dados dos usuários para o AG-Grid
    """
    try:
        users = User.objects.all().values(
            'id', 'first_name', 'last_name', 'email', 
            'birthdate', 'gender', 'user_type', 'is_active', 'date_joined',
            'cpf', 'phone', 'profile_completed'
        )
        
        users_list = []
        for user in users:
            # Calcular idade se birthdate existir
            age = None
            if user['birthdate']:
                today = date.today()
                age = today.year - user['birthdate'].year - ((today.month, today.day) < (user['birthdate'].month, user['birthdate'].day))
            
            users_list.append({
                'id': user['id'],
                'full_name': f"{user['first_name']} {user['last_name']}",
                'email': user['email'],
                'age': age,
                'gender_display': dict([('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')]).get(user['gender'], 'Não informado'),
                'user_type_display': dict([('A', 'Admin'), ('U', 'Usuário'), ('O', 'Observer')]).get(user['user_type'], 'Usuário'),
                'user_type_code': user['user_type'],  # Adicionar código do tipo para o select
                'is_active': user['is_active'],
                'date_joined_formatted': user['date_joined'].strftime('%d/%m/%Y') if user['date_joined'] else '',
            })
        
        return JsonResponse({'users': users_list})
    except Exception as e:
        return handle_json_error(f'Erro ao carregar usuários: {str(e)}', 500)


@staff_member_required
def admin_gender_stats(request):
    """
    API para estatísticas de gênero dos usuários (gráfico pizza)
    """
    try:
        gender_stats = User.objects.values('gender').annotate(count=Count('gender'))
        
        data = []
        total_users = User.objects.count()
        
        for stat in gender_stats:
            gender_label = dict([('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')]).get(stat['gender'], 'Não informado')
            percentage = round((stat['count'] / total_users) * 100, 1) if total_users > 0 else 0
            
            data.append({
                'label': gender_label,
                'value': stat['count'],
                'percentage': percentage
            })
        
        return JsonResponse({'data': data})
    except Exception as e:
        return handle_json_error(f'Erro ao carregar estatísticas de gênero: {str(e)}', 500)


@staff_member_required
def admin_age_stats(request):
    """
    API para estatísticas de idade dos usuários (gráfico barra)
    """
    try:
        users_with_birthdate = User.objects.filter(birthdate__isnull=False)
        
        age_ranges = {
            '18-25': 0,
            '26-35': 0,
            '36-45': 0,
            '46-55': 0,
            '56+': 0
        }
        
        today = date.today()
        
        for user in users_with_birthdate:
            age = today.year - user.birthdate.year - ((today.month, today.day) < (user.birthdate.month, user.birthdate.day))
            
            if 18 <= age <= 25:
                age_ranges['18-25'] += 1
            elif 26 <= age <= 35:
                age_ranges['26-35'] += 1
            elif 36 <= age <= 45:
                age_ranges['36-45'] += 1
            elif 46 <= age <= 55:
                age_ranges['46-55'] += 1
            elif age > 55:
                age_ranges['56+'] += 1
        
        data = [{'label': k, 'value': v} for k, v in age_ranges.items()]
        
        return JsonResponse({'data': data})
    except Exception as e:
        return handle_json_error(f'Erro ao carregar estatísticas de idade: {str(e)}', 500)



@staff_member_required
def admin_user_delete(request, user_id):
    """
    API para deletar usuário
    """
    if request.method != 'DELETE':
        return handle_json_error('Método não permitido', 405)
    
    try:
        user = get_object_or_404(User, id=user_id)
        
        # Não permitir deletar o próprio usuário
        if user.id == request.user.id:
            return handle_json_error('Não é possível deletar seu próprio usuário')
        
        user_name = f"{user.first_name} {user.last_name}"
        user.delete()
        
        return handle_json_success(f'Usuário "{user_name}" removido com sucesso!')
        
    except User.DoesNotExist:
        return handle_json_error('Usuário não encontrado', 404)
    except Exception as e:
        return handle_json_error(f'Erro interno: {str(e)}', 500)

@staff_member_required
def admin_user_deactivate(request, user_id):
    """
    API para desativar usuário
    """
    if request.method != 'POST':
        return handle_json_error('Método não permitido', 405)
    
    try:
        user = get_object_or_404(User, id=user_id)
        
        if user.id == request.user.id:
            return handle_json_error('Não é possível desativar seu próprio usuário')
        
        user.is_active = False
        user.save()
        
        return handle_json_success(f'Usuário "{user.email}" desativado com sucesso!')

    except User.DoesNotExist:
        return handle_json_error('Usuário não encontrado', 404)
    except Exception as e:
        return handle_json_error(f'Erro interno: {str(e)}', 500)
    
@staff_member_required
def admin_user_activate(request, user_id):
    """
    API para ativar usuário
    """
    if request.method != 'POST':
        return handle_json_error('Método não permitido', 405)
    
    try:
        user = get_object_or_404(User, id=user_id)
        
        if user.id == request.user.id:
            return handle_json_error('Não é possível ativar seu próprio usuário')
        
        user.is_active = True
        user.save()
        
        return handle_json_success(f'Usuário "{user.email}" ativado com sucesso!')
    except User.DoesNotExist:
        return handle_json_error('Usuário não encontrado', 404)
    except Exception as e:
        return handle_json_error(f'Erro interno: {str(e)}', 500)


