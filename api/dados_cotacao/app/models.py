from django.db import models

class DataSolModel(models.Model):
    DataSolicitada = models.DateField(auto_now=False, auto_now_add=False,primary_key=True)
    DolarSolicitado = models.IntegerField()
    DolarAtual = models.IntegerField()
    