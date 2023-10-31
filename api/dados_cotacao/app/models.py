from django.db import models

class DataSolModel(models.Model):
    DataSolicitada = models.CharField(primary_key=True)
    DolarSolicitado = models.FloatField()
    DolarAtual = models.FloatField()
    