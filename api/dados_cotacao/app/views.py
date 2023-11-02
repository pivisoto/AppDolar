from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import DataSolModel
import requests
from rest_framework.decorators import api_view

#obtem o valor da cotação do dólar atual e da data que foi solicitado
def ObtemCotacaoBancoCentral(data_solicitada):
    #formatação para que a api do banco central aceite a data
    data_solicitada = datetime.strptime(data_solicitada, '%Y-%m-%d')
    DataSolicitadaFormatada = data_solicitada.strftime('%m-%d-%Y')
    print(DataSolicitadaFormatada)
    url_DolarSolicitado = f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao=\'{DataSolicitadaFormatada}\'&$top=100&$format=json&$select=cotacaoCompra'
    #busca e armazena o response da api (json)
    try:
        responseDolarSolicitado = requests.get(url_DolarSolicitado)
        dataDolarSolicitado = responseDolarSolicitado.json()
        
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
        

def procuraDataValida():
    UmDia = timedelta(days=1)
    DoisDias = timedelta(days=2)
    DataAtual = datetime.now()
    if DataAtual.weekday() not in [0,5,6]:
        if DataAtual.hour > 13:
            DataAtual = DataAtual.strftime('%m-%d-%Y')
            return DataAtual
        else:
            DataAtual = DataAtual - UmDia
            DataAtual.strftime('%m-%d-%Y')
            return DataAtual
    else:
        if DataAtual.weekday() == 0:
            if DataAtual.hour > 13:
                DataAtual.strftime('%m-%d-%Y')
                return DataAtual
            else:
                DataAtual = DataAtual - DoisDias
                DataAtual = DataAtual.strftime('%m-%d-%Y')
                return DataAtual
        else:
            if DataAtual.weekday() == 5:
                DataAtual = DataAtual - UmDia
                DataAtual = DataAtual.strftime('%m-%d-%Y')
                return DataAtual
            else:
                DataAtual = DataAtual - DoisDias
                DataAtual = DataAtual.strftime('%m-%d-%Y')
                return DataAtual
    
def procuraDolarAtual():
    DataAtual = procuraDataValida()
    #Codigo que garante que a data da cotação seja valida para a api do banco central
    url_DolarAtual= f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao=\'{DataAtual}\'&$top=100&$format=json&$select=cotacaoCompra'
    try:
        responseDolarAtual = requests.get(url_DolarAtual)
        dataDolarAtual = responseDolarAtual.json()
        if 'value' in dataDolarAtual and len(dataDolarAtual['value']) > 0:
            DolarAtual = dataDolarAtual['value'][0]['cotacaoCompra']
            return DolarAtual
        else:
            raise Exception("Nenhum resultado encontrado para a data especificada")
    except:
        raise Exception("Erro de solicitação para a API do Banco Central")


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
        
@api_view(['GET']) 
def EnviaCotacao(request, data_solicitada):
    try:
        DolarAtual = procuraDolarAtual()
        CotacaoExistente = DataSolModel.objects.filter(DataSolicitada=data_solicitada).first()
        if CotacaoExistente:
            ResponseData = {
                'DolarSolicitado': CotacaoExistente.DolarSolicitado,
                'DolarAtual' : DolarAtual,
            }
            return JsonResponse(ResponseData)
        DolarSolicitado = ObtemCotacaoBancoCentral(data_solicitada)
        if DolarSolicitado is not None:
            ResponseData = {
                'DolarSolicitado': DolarSolicitado,
                'DolarAtual' : DolarAtual,
            }
            return JsonResponse(ResponseData)
        else:
            return JsonResponse({'mensagem': 'cotação não existe'}, status=400)
    except Exception:
        return JsonResponse({'mensagem': f'Erro: erro correia'}, status=400)