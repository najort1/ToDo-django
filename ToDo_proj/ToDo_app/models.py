from django.db import models

# Create your models here.
class Task(models.Model):
    
    class Status(models.TextChoices):
        PENDING = 'PENDENTE'
        IN_PROGRESS = 'EM ANDAMENTO'
        COMPLETED = 'COMPLETADO'
    
    
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
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
