from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def register(request):
    if request.user.is_authenticated:
        return redirect('tasks:dashboard')  # Redireciona para a página principal se já estiver logado
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.first_name}! Sua conta foi criada com sucesso.')
            return redirect('tasks:dashboard')  # Redireciona para a página principal após o cadastro

        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('tasks:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.first_name}!')
            
            # Redireciona para a página que o usuário estava tentando acessar ou para a página principal
            next_page = request.GET.get('next', 'tasks:dashboard')
            return redirect(next_page)
        else:
            messages.error(request, 'Por favor, verifique suas credenciais.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        user_name = request.user.first_name
        auth_logout(request)
        messages.success(request, f'Até logo, {user_name}! Você foi desconectado com sucesso.')
    
    return redirect('tasks:index')
