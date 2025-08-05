from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from email_validator import validate_email, EmailNotValidError
import re



class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite seu nome',
            'id': 'first_name'
        }),
        label='Nome'
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite seu sobrenome',
            'id': 'last_name'
        }),
        label='Sobrenome'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite seu email',
            'id': 'email'
        }),
        label='Email'
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite sua senha',
            'id': 'password1'
        }),
        label='Senha'
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirme sua senha',
            'id': 'password2'
        }),
        label='Confirmar Senha'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Validação robusta de email usando email-validator
        try:
            emailinfo = validate_email(email, check_deliverability=False)
            email = emailinfo.normalized
        except EmailNotValidError as e:
            raise ValidationError(f'Email inválido: {str(e)}')
        
        # Verificar se o email já está em uso
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email já está em uso.')
        elif User.objects.filter(username=email).exists():
            raise ValidationError('Este email já está em uso.')
        
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.replace(' ', '').isalpha():
            raise ValidationError('O nome deve conter apenas letras.')
        if len(first_name.strip()) < 2:
            raise ValidationError('O nome deve ter pelo menos 2 caracteres.')
        return first_name.strip().title()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.replace(' ', '').isalpha():
            raise ValidationError('O sobrenome deve conter apenas letras.')
        if len(last_name.strip()) < 2:
            raise ValidationError('O sobrenome deve ter pelo menos 2 caracteres.')
        return last_name.strip().title()

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        # Validações de senha forte
        if len(password1) < 8:
            raise ValidationError('A senha deve ter pelo menos 8 caracteres.')
        
        if not re.search(r'[A-Z]', password1):
            raise ValidationError('A senha deve conter pelo menos uma letra maiúscula.')
        
        if not re.search(r'[a-z]', password1):
            raise ValidationError('A senha deve conter pelo menos uma letra minúscula.')
        
        if not re.search(r'\d', password1):
            raise ValidationError('A senha deve conter pelo menos um número.')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise ValidationError('A senha deve conter pelo menos um caractere especial.')
        
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite seu email',
            'id': 'email'
        }),
        label='Email'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite sua senha',
            'id': 'password'
        }),
        label='Senha'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Validação robusta de email usando email-validator
        try:
            emailinfo = validate_email(username, check_deliverability=False)
            username = emailinfo.normalized
        except EmailNotValidError as e:
            raise ValidationError(f'Email inválido: {str(e)}')
        
        
        return username

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Tentar autenticar com o email como username
            self.user_cache = authenticate(
                self.request, 
                username=username, 
                password=password
            )
            if self.user_cache is None:
                raise ValidationError('Email ou senha incorretos.')
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data