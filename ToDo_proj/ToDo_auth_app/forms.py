from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from email_validator import validate_email, EmailNotValidError
from .services import testa_cpf
from ToDo_user_app.models import Address
from ToDo_user_app import choices as ch

import re
import datetime

User = get_user_model()



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
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'birthdate', 'gender', 'cpf')


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
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:  # Só valida se foi fornecido
            if not cpf.isdigit():
                raise ValidationError('O CPF deve conter apenas números.')
            if len(cpf) != 11:
                raise ValidationError('O CPF deve conter 11 dígitos.')
            if not testa_cpf(cpf):
                raise ValidationError('CPF inválido.')
            if User.objects.filter(cpf=cpf).exists():
                raise ValidationError('Este CPF já está em uso.')
        return cpf
    
    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate:
            if birthdate > datetime.date.today():
                raise ValidationError('A data de nascimento não pode ser futura.')
        return birthdate
    
    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if gender and gender not in [choice[0] for choice in ch.Gender.choices]:
            raise ValidationError('Gênero inválido.')
        return gender



    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
            
        if commit:
            user.save()
        return user


# Formulário para a segunda etapa do cadastro
class SecondStepRegistrationForm(forms.Form):
    # Campos obrigatórios da segunda etapa
    birthdate = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite sua data de nascimento',
            'id': 'birthdate',
            'type': 'date'
        }),
        label='Data de Nascimento'
    )
    
    gender = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-input',
            'id': 'gender'
        }),
        label='Gênero',
        choices=[('', 'Selecione seu gênero')] + list(ch.Gender.choices)
    )
    
    cpf = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite seu CPF (apenas números)',
            'id': 'cpf',
        }),
        label='CPF'
    )
    
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite seu telefone',
            'id': 'phone'
        }),
        label='Telefone'
    )
    
    # Campos de endereço
    zipcode = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite o CEP',
            'id': 'zipcode',
            'maxlength': '9'
        }),
        label='CEP'
    )
    
    street = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite o nome da rua',
            'id': 'street'
        }),
        label='Rua'
    )
    
    number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite o número',
            'id': 'number'
        }),
        label='Número'
    )
    
    complement = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Complemento (opcional)',
            'id': 'complement'
        }),
        label='Complemento'
    )
    
    neighborhood = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite o bairro',
            'id': 'neighborhood'
        }),
        label='Bairro'
    )
    
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Digite a cidade',
            'id': 'city'
        }),
        label='Cidade'
    )
    
    state = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-input',
            'id': 'state'
        }),
        label='Estado',
        choices=[('', 'Selecione o estado')] + list(ch.States.choices)
    )
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        real_cpf_clean = re.sub(r'\D', '', cpf)

        if not real_cpf_clean.isdigit():
            raise ValidationError('O CPF deve conter apenas números.')
        if len(real_cpf_clean) != 11:
            raise ValidationError('O CPF deve conter 11 dígitos.')
        if not testa_cpf(real_cpf_clean):
            raise ValidationError('CPF inválido.')
        if User.objects.filter(cpf=real_cpf_clean).exists():
            raise ValidationError('Este CPF já está em uso.')
        return real_cpf_clean

    
    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate > datetime.date.today():
            raise ValidationError('A data de nascimento não pode ser futura.')
        return birthdate
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        real_phone_clean = re.sub(r'\D', '', phone)
        if not real_phone_clean.isdigit():
            raise ValidationError('O telefone deve conter apenas números.')
        if len(real_phone_clean) < 10 or len(real_phone_clean) > 11:
            raise ValidationError('Telefone deve ter 10 ou 11 dígitos.')
        return real_phone_clean
    
    def clean_zipcode(self):
        zipcode = self.cleaned_data.get('zipcode')
        # Remove caracteres não numéricos
        zipcode_digits = re.sub(r'\D', '', zipcode)
        if len(zipcode_digits) != 8:
            raise ValidationError('CEP deve ter 8 dígitos.')
        return zipcode_digits


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