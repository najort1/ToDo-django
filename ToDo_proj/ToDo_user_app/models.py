from django.db import models
from . import choices as ch
from django.contrib.auth.models import AbstractUser



# Create your models here.
class Usuario(AbstractUser):
    birthdate = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    gender = models.CharField(max_length=1, choices=ch.Gender.choices, null=True, blank=True, verbose_name="Gênero")
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True, verbose_name="CPF")
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Telefone")
    user_type = models.CharField(max_length=1, choices=ch.User_type.choices, null=False, blank=False, default=ch.User_type.USER, verbose_name="Tipo de Usuário")
    next_step = models.BooleanField(null=False, blank=False, default=False, verbose_name="Próximo Passo")
    profile_completed = models.BooleanField(null=False, blank=False, default=False, verbose_name="Perfil Completo")


    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
    
    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"


class Address(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")
    zipcode = models.CharField(max_length=9, null=False, blank=False, verbose_name="CEP")
    street = models.CharField(max_length=100, null=False, blank=False, verbose_name="Rua")
    number = models.CharField(max_length=10, null=False, blank=False, verbose_name="Número")
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    neighborhood = models.CharField(max_length=100, null=False, blank=False, verbose_name="Bairro")
    city = models.CharField(max_length=100, null=False, blank=False, verbose_name="Cidade")
    state = models.CharField(max_length=2, choices=ch.States.choices, null=False, blank=False, verbose_name="Estado")
    formatted_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço Formatado")

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def save(self, *args, **kwargs):
        # Gera o endereço formatado automaticamente
        address_parts = [
            f"{self.street}, {self.number}",
            self.complement if self.complement else None,
            self.neighborhood,
            f"{self.city}/{self.state}",
            self.zipcode
        ]
        # Remove partes vazias e junta com " - "
        self.formatted_address = " - ".join(filter(None, address_parts))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}/{self.state}"