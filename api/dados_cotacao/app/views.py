from django.shortcuts import render
from rest_framework import views, status;
import requests;
import datetime;
from rest_framework.response import Response;
from  app.serializer import DataSolicitadaSerializer;
from app.models import *;
from django.http import JsonResponse
from datetime import datetime
import requests

#obtem o valor da cotação do dólar atual e da data que foi solicitado
def ObtemCotacao(data_solicitada):
    #formatação para que a api do banco central aceite a data
    data_solicitada = datetime.strptime(data_solicitada, '%Y-%m-%d')
    DataSolicitadaFormatada = data_solicitada.strftime('%m-%d-%Y')
    url_DolarSolicitado = f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao=\'{DataSolicitadaFormatada}\'&$top=1&$skip=0&$format=json'

    #obtem a data atual e formata
    DataAtual = datetime.now()
    DataAtualFormatada = DataAtual.strftime('%m-%d-%Y')
    url_DolarAtual = f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao=\'{DataAtualFormatada}\'&$top=1&$skip=0&$format=json'
    
    #busca e armazena o response da api (json)
    try:
        responseDolarSolicitado = requests.get(url_DolarSolicitado)
        dataDolarSolicitado = responseDolarSolicitado.json()
        
        responseDolarAtual = requests.get(url_DolarAtual)
        dataDolarAtual = responseDolarAtual.json()
        
        #verifica se algum valor foi retornado , em caso positivo adiciona os valores a variavel DolarSolicitado e DolarAtual
        #caso contrario retorna uma mensagem que nenhum valor foi encontrado
        if 'value' in dataDolarSolicitado and len(dataDolarSolicitado['value']) > 0:
            DolarSolicitado = dataDolarSolicitado['value'][0]['cotacaoCompra']
            DolarAtual = dataDolarAtual['value'][0]['cotacaoCompra']
            return DolarSolicitado,DolarAtual
        else:
            raise Exception("Nenhum resultado encontrado para a data especificada")
    except:
        raise Exception("Erro de solicitação para a API do Banco Central")
        
                
def VerificaCotacao(request):
    if request.method == 'GET':
        data_solicitada = request.GET.get('data')

        DolarSolicitado , DolarAtual = ObtemCotacao(data_solicitada)

        if DolarSolicitado  is not None and DolarAtual is not None:
            RetornaValores = {
                'DataSolicitada': data_solicitada,
                'DolarSolicitado': DolarSolicitado ,
                'DolarAtual': DolarAtual
            }
            return JsonResponse(RetornaValores)
        else:
            return JsonResponse({'mensagem': 'Falha ao obter cotação do Banco Central'}, status=400)
                
class DataSolView(views.APIView):
    def post(self, request):
        serializer = DataSolicitadaSerializer(data=request.data)
        if serializer.is_valid():
            datasol = DataSolModel(**serializer.validated_data)
            return Response(DataSolicitadaSerializer(datasol).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)