from flask import Flask, request, jsonify#  request ira servir para pegar o payload, jsonify vai servir para forncer os dados no formato json
from flask_basicauth import BasicAuth
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import pickle
import os

# treinamento do modelo
# so vai ser executado uma vez ao lancar o app
colunas = ['tamanho', 'ano', 'garagem'] # vamos usar variavel para garantir que as colunas sigam a ordem correta
modelo = pickle.load(open('modelo.sav', 'rb'))


app = Flask(__name__) # cria o app
# é uma boa pratica passar a variavel especial do python __name_
# assim fica mais de saber onde essa aplicacao esta rodando
# e facilita para o flask encontrar os recursos dessa aplicacao

# autenticacao basica da API
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_autentication = BasicAuth(app) # precisamos colocar a autenticacao a cada endpoint

@app.route('/') # diz qual rota o usuario deve usar para chegar nessa pagina. '/' indica que e a rota home
def home(): # o que deve ser feito quando o usuario chegar nessa rota
    return "minha primeira API."


# endpoint e a URL de acesso a nossa aplicacao (ou pontos de acesso para nossa aplicacao)
# vamos criar um endpoint para nosso modelo
@app.route('/sentimento/<frase>') 
@basic_autentication.required # identificando que para esse endpoint, precisa de autenticacao
# esse endpoint recebe uma frase do usuário e retorna a polaridade (sentimento)
# o valor da frase está sendo passado na URL
def sentimento(frase):
    frase = frase
    tb = TextBlob(frase)
    polaridade = tb.sentiment.polarity
    return "A polaridade é: {}".format(polaridade)


# criando um novo endpoint para o outro modelo
@app.route('/cotacao/', methods=['POST']) # por padrao e usado o GET (foi usado no sentimento), porem, como queremos receber varios dados, vamos usar o metodo POST
# esse conjunto de dados que vamos receber costuma ser chamado de payload
def cotacao():
    
    dados2 = request.get_json() # para pegar o json enviado pelo usuario
    # agora, vamos preparar esse arquivo json para o modelo, vamos colocar na ordem
    dados_input = [dados2[col] for col in colunas]
    preco = modelo.predict([dados_input])
    # é interessante devolver o dado no formato jason tambem, ja que o desenvolver pode trabalhar em cima do resultado do modelo
    # antes de servir ao usuário
    return jsonify(preco=preco[0])
app.run(debug=True) # roda o aplicativo quando o codigo e executado
# quando o debug esta ON, o flask vai restartar a aplicacao automaticamente