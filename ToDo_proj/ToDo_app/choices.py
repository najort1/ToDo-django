from django.db import models

class Status(models.TextChoices):
    PENDING = 'PENDENTE', 'Pendente'
    IN_PROGRESS = 'EM ANDAMENTO', 'Em Andamento'
    COMPLETED = 'COMPLETADO', 'Concluído'


class Months(models.TextChoices):
    JANUARY = '01', 'Janeiro'
    FEBRUARY = '02', 'Fevereiro'
    MARCH = '03', 'Março'
    APRIL = '04', 'Abril'
    MAY = '05', 'Maio'
    JUNE = '06', 'Junho'
    JULY = '07', 'Julho'
    AUGUST = '08', 'Agosto'
    SEPTEMBER = '09', 'Setembro'
    OCTOBER = '10', 'Outubro'
    NOVEMBER = '11', 'Novembro'
    DECEMBER = '12', 'Dezembro'
