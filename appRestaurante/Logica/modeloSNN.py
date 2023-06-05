from django.urls import reverse
from keras import backend as K
from appRestaurante.Logica import modeloSNN
from keras.models import load_model
from sklearn.pipeline import Pipeline
import pickle
import json
import pandas as pd
from keras.preprocessing.text import tokenizer_from_json
from keras_preprocessing.sequence import pad_sequences

class modeloSNN():
    """Clase modelo Preprocesamiento y RNN"""
    def tokenizar(self, text):
        text = [text]
        tokenizer=self.cargarTokenizer(self,'Recursos/tokenizerPreprocesadores')
        x = tokenizer.texts_to_sequences(text)
        padded_sequences = pad_sequences(x, maxlen=81, padding='pre')
        x = pad_sequences(padded_sequences)
        x = pd.DataFrame(x)
        x
        return x
    def cargarNuevoPipe(self):
        pipe = Pipeline(steps=[])
        print('Nuevo pipeline cargado')
        return pipe
    def cargarRNN(self, nombreArchivo):
        model = load_model(nombreArchivo+'.h5')
        print('Red Neuronal Cargada desde Archivo')
        return model
    def cargarTokenizer(self, nombreArchivo):
        with open(nombreArchivo+'.json') as f:
            data = json.load(f)
            tokenizer = tokenizer_from_json(data)
        return tokenizer
    def cargarModelo(self):
        modeloOptimizado = self.cargarRNN(self,'Recursos/modeloRedNeuronalOptimizada')  
        return modeloOptimizado
    def predecir(self, t):
        Xnew = self.tokenizar(self, t)
        print(Xnew.shape)
        pipe = self.cargarNuevoPipe(self)
        modeloOptimizado = self.cargarModelo(self)
        pipe.steps.append(['modelNN',modeloOptimizado])
        prediccion = (pipe.predict(Xnew)> 0.5).astype("int32")
        prediccion = prediccion.flatten()[0]
        dic = {0:'malo' , 1:'bueno', 2:'excelente'}
        if prediccion<3:
            prediccion={ "sentimiento": dic[prediccion]}
        return prediccion