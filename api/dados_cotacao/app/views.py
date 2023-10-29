from django.shortcuts import render
from rest_framework import views, status;
from rest_framework.response import Response;
from  app.serializer import DataSolicitadaSerializer;
from app.models import *;

class DataSolView(views.APIView):
    def post(self, request):
        serializer = DataSolicitadaSerializer(data=request.data)
        if serializer.is_valid():
            datasol = DataSolModel(**serializer.validated_data)
            return Response(DataSolicitadaSerializer(datasol).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)