from django.db import models
from .cidade import Cidade

class Endereco(models.Model):
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    logradouro = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.logradouro}, {self.cidade}"
