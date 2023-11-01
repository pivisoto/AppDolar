from django.shortcuts import render
from rest_framework import views, status;
import requests;
import datetime;
from rest_framework.response import Response;
from  app.serializer import DataSolicitadaSerializer;
from app.models import DataSolModel;
from django.http import JsonResponse
from datetime import datetime
from .models import DataSolModel
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

#obtem o valor da cotação do dólar atual e da data que foi solicitado
def ObtemCotacaoBancoCentral(data_solicitada):
    #formatação para que a api do banco central aceite a data
    data_solicitada = datetime.strptime(data_solicitada, '%Y-%m-%d')
    DataSolicitadaFormatada = data_solicitada.strftime('%m-%d-%Y')
    print(DataSolicitadaFormatada)
    url_DolarSolicitado = f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao=\'{DataSolicitadaFormatada}\'&$top=100&$format=json&$select=cotacaoCompra'

    # Obtem a data atual e formata
    #DataAtual = datetime.now().strftime('%m-%d-%Y')
    # DataAtual = '10-31-2023'
    # print(DataAtual)
    # url_DolarAtual = f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao=\'{DataAtual}\'&$top=1&$skip=0&$format=json'
    
    #busca e armazena o response da api (json)
    try:
        responseDolarSolicitado = requests.get(url_DolarSolicitado)
        dataDolarSolicitado = responseDolarSolicitado.json()
        
        # responseDolarAtual = requests.get(url_DolarAtual)
        # dataDolarAtual = responseDolarAtual.json()
        
        #verifica se algum valor foi retornado , em caso positivo adiciona os valores a variavel DolarSolicitado e DolarAtual
        #caso contrario retorna uma mensagem que nenhum valor foi encontrado
        if 'value' in dataDolarSolicitado and len(dataDolarSolicitado['value']) > 0:
            DolarSolicitado = dataDolarSolicitado['value'][0]['cotacaoCompra']
            # DolarAtual = dataDolarAtual['value'][0]['cotacaoCompra']
            return DolarSolicitado
        else:
            raise Exception("Nenhum resultado encontrado para a data especificada")
    except:
        raise Exception("Erro de solicitação para a API do Banco Central")
        
                
# def SalvaCotacaoBancoCentral(request,data_solicitada):
#     if request.method == 'GET':
#         data_solicitada = request.GET.get('data')
#         DolarSolicitado , DolarAtual = ObtemCotacaoBancoCentral(data_solicitada)

#         if DolarSolicitado  is not None and DolarAtual is not None:
#             NovaCotacao = DataSolModel(
#                 DataSolicitada = data_solicitada,
#                 DolarSolicitado =  DolarSolicitado ,
#                 DolarAtual =  DolarAtual
#             )
#             return NovaCotacao.save()
#         else:
#             return JsonResponse({'mensagem': 'Falha ao obter cotação do Banco Central'}, status=400)
        
# def VerificaBancoDados(data_solicitada):
#     try:
#         cotacao_existente = DataSolModel.objects.get(DataSolicitada=data_solicitada)
#         return True
#     except DataSolModel.DoesNotExist:
#         return False

# def VerificaEObtemCotacao(data_solicitada):
#     if VerificaBancoDados(data_solicitada):
#         cotacao_existente = DataSolModel.objects.get(DataSolicitada=data_solicitada)
#         DataSolicitada = cotacao_existente.DataSolicitada
#         DolarSolicitado = cotacao_existente.DolarSolicitado
#         DolarAtual = cotacao_existente.DolarAtual
#         return cotacao_existente
#     else:
#         DolarSolicitado, DolarAtual = ObtemCotacaoBancoCentral(data_solicitada)
#         return False

@api_view(['POST']) 
def Cotacao(request,data_solicitada):
    try:
        cotacao_existente = DataSolModel.objects.filter(DataSolicitada=data_solicitada).first()
        if cotacao_existente:
            return JsonResponse({'mensagem': 'A cotação já existe no banco'})
        DolarSolicitado = ObtemCotacaoBancoCentral(data_solicitada)
        if DolarSolicitado is not None:
            # Salva a cotação no banco de dados
            DataSolModel.objects.create(
                DataSolicitada=data_solicitada,
                DolarSolicitado=DolarSolicitado
            )
            return JsonResponse({'mensagem': 'A cotação foi cadastrada no banco'})
        else:
            return JsonResponse({'mensagem': 'Falha ao obter cotação do Banco Central'}, status=400)
    except Exception as e:
        return JsonResponse({'mensagem': f'Erro: {str(e)}'}, status=400)


