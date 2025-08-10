from django.db import models
from django.conf import settings
from .choices import Status


# Create your models here.
class Task(models.Model):
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Usuário',
        help_text='Usuário que criou a tarefa'

    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Status',
        help_text='Status da tarefa'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em', help_text='Data de criação da tarefa')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em', help_text='Data de atualização da tarefa')

    def __str__(self):
        return f'{self.title} - {self.status}'