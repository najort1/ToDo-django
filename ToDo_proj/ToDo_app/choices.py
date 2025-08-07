from django.db import models

class Status(models.TextChoices):
    PENDING = 'PENDENTE', 'Pendente'
    IN_PROGRESS = 'EM ANDAMENTO', 'Em Andamento'
    COMPLETED = 'COMPLETADO', 'Concluído'
