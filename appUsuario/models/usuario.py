from django.db import models
from .grau_escolaridade import GrauEscolaridade
from .area_interesse import AreaInteresse
from .profissao import Profissao
from .endereco import Endereco

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    celular = models.CharField(max_length=20)

    grau_escolaridade = models.ForeignKey(GrauEscolaridade, on_delete=models.SET_NULL, null=True)
    instituicao_ensino = models.CharField(max_length=255)
    area_interesse = models.ForeignKey(AreaInteresse, on_delete=models.SET_NULL, null=True)
    profissao = models.ForeignKey(Profissao, on_delete=models.SET_NULL, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
