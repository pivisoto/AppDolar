from rest_framework import serializers
from .models import *

class DataSolicitadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSolModel   
        fields = ['DataSolicitada','DolarSolicitado','DolarAtual']