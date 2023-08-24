from django.db import models

# Create your models here.


class Conta(models.Model):
    conta_id = models.IntegerField(verbose_name="Numero da Conta")
    saldo = models.FloatField(verbose_name="Saldo")

    def __str__(self):
        return f"{self.conta_id} {self.saldo}"
