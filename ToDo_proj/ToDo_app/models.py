from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    
    class Status(models.TextChoices):
        PENDING = 'PENDENTE'
        IN_PROGRESS = 'EM ANDAMENTO'
        COMPLETED = 'COMPLETADO'
    
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.status}'
