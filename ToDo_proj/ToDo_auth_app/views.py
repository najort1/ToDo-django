from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, SecondStepRegistrationForm
from ToDo_user_app.models import Address


def register(request):
    if request.user.is_authenticated:
        if not request.user.next_step:
            return redirect('tasks:dashboard')
        else:
            return redirect('auth:register_step2')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.next_step = True
            user.save()
            
            auth_login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.first_name}! Agora complete seu cadastro.')
            return redirect('auth:register_step2')

        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.next_step:
            return redirect('auth:register_step2')
        return redirect('tasks:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            
            if user.next_step:
                messages.info(request, f'Bem-vindo de volta, {user.first_name}! Complete seu cadastro.')
                return redirect('auth:register_step2')
            
            messages.success(request, f'Bem-vindo de volta, {user.first_name}!')
            
            # Redireciona para a página que o usuário estava tentando acessar ou para a página principal
            next_page = request.GET.get('next', 'tasks:dashboard')
            return redirect(next_page)
        else:
            messages.error(request, 'Por favor, verifique suas credenciais.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})


@login_required
def register_step2(request):
    if not request.user.next_step:
        messages.info(request, 'Seu cadastro já está completo!')
        return redirect('tasks:dashboard')
    
    if request.method == 'POST':
        form = SecondStepRegistrationForm(request.POST)
        if form.is_valid():
            user = request.user
            user.birthdate = form.cleaned_data['birthdate']
            user.gender = form.cleaned_data['gender']
            user.cpf = form.cleaned_data['cpf']
            user.phone = form.cleaned_data['phone']
            user.next_step = False
            user.profile_completed = True
            user.save()
            
            # Cria ou atualiza o endereço
            address, created = Address.objects.get_or_create(
                user=user,
                defaults={
                    'street': form.cleaned_data['street'],
                    'number': form.cleaned_data['number'],
                    'complement': form.cleaned_data.get('complement', ''),
                    'neighborhood': form.cleaned_data['neighborhood'],
                    'city': form.cleaned_data['city'],
                    'state': form.cleaned_data['state'],
                    'zipcode': form.cleaned_data['zipcode'],
                }
            )
            
            if not created:
                address.street = form.cleaned_data['street']
                address.number = form.cleaned_data['number']
                address.complement = form.cleaned_data.get('complement', '')
                address.neighborhood = form.cleaned_data['neighborhood']
                address.city = form.cleaned_data['city']
                address.state = form.cleaned_data['state']
                address.zipcode = form.cleaned_data['zipcode']
                address.save()
            
            messages.success(request, 'Cadastro completo! Bem-vindo ao sistema.')
            return redirect('tasks:dashboard')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = SecondStepRegistrationForm()
        

    
    return render(request, 'auth/register_step2.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        user_name = request.user.first_name
        auth_logout(request)
        messages.success(request, f'Até logo, {user_name}! Você foi desconectado com sucesso.')
    
    return redirect('tasks:index')

def delete_account(request):
    if request.user.is_authenticated:
        user = request.user
        user.delete()
        messages.success(request, 'Sua conta foi deletada com sucesso.')
        return redirect('tasks:index')
    else:
        messages.error(request, 'Você precisa estar logado para deletar sua conta.')
        return redirect('auth:login')
