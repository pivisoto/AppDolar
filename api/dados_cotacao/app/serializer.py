from rest_framework import serializers
from .models import DataSolModel

class DataSolicitadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSolModel  
        fields = ['datasolicitada','dolarsolicitado']