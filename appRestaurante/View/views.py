from django.shortcuts import render
from appRestaurante.Logica import modeloSNN
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse

class Clasificacion():
    def determinarComentario(request):
        return render(request, "nuevoComentario.html")
    @api_view(['GET','POST'])
    def predecir(request):
        try:
            COMENTARIO=str(request.POST.get('COMENTARIO'))
            resul=modeloSNN.modeloSNN.predecir(modeloSNN.modeloSNN, COMENTARIO)
        except:
            resul='Datos inválidos'
        return render(request, "informe.html",{"e":resul})
    @csrf_exempt
    @api_view(['GET','POST'])
    def predecirIOJson(request):
        print(request)
        print('***')
        print(request.body)
        print('***')
        print('Leer comentario')
        print(request.POST.get('COMENTARIO'))
        #Formato de datos de entrada
        resul=modeloSNN.modeloSNN.predecir(modeloSNN.modeloSNN, request.POST.get('COMENTARIO'))
        data = {'result': resul}
        resp=JsonResponse(data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp