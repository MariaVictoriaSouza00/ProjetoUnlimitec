from django.db import models

class Estado(models.Model):
    sigla = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.sigla
