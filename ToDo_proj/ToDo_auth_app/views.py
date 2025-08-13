from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, SecondStepRegistrationForm
from django.views.generic import DeleteView, FormView, ListView, CreateView, UpdateView,DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class AuthRegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'auth/register.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.next_step:
                return redirect('auth:register_step2')
            return redirect('tasks:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        user.next_step = True
        user.save()
        auth_login(self.request, user)
        messages.success(self.request, f'Bem-vindo(a), {user.first_name}! Agora complete seu cadastro.')
        return redirect("auth:register_step2")
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija os erros abaixo.')
        return super().form_invalid(form)

    

class AuthLoginView(FormView):
    form_class = CustomAuthenticationForm
    template_name = 'auth/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.next_step:
                return redirect('auth:register_step2')
            return redirect('tasks:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        
        if user.next_step:
            messages.info(self.request, f'Bem-vindo de volta, {user.first_name}! Complete seu cadastro.')
            return redirect('auth:register_step2')
            
        messages.success(self.request, f'Bem-vindo de volta, {user.first_name}!')
        return redirect('tasks:dashboard')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija os erros abaixo.')
        return super().form_invalid(form)


class AuthRegisterStep2(LoginRequiredMixin, FormView):
    form_class = SecondStepRegistrationForm
    template_name = 'auth/register_step2.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.next_step:
            messages.info(request, 'Seu cadastro já está completo!')
            return redirect('tasks:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.save(self.request.user)
        messages.success(self.request, 'Cadastro completo! Bem-vindo ao sistema.')
        return redirect('tasks:dashboard')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija os erros abaixo.')
        return super().form_invalid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        messages.success(request, 'Você foi desconectado com sucesso.')
        return redirect('tasks:index')

class DeleteAccountView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        messages.success(request, 'Sua conta foi deletada com sucesso.')
        return redirect('tasks:index')