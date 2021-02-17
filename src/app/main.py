from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
import pickle
import os

DIR_APP = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_MODELO = os.path.join(DIR_APP, "models", "modelo.sav")

colunas = ['tamanho','ano','garagem']
modelo = pickle.load(open(DIR_MODELO,'rb'))

app = Flask(__name__)

print('user', os.environ.get('BASIC_AUTH_USERNAME'))
print('senha', os.environ.get('BASIC_AUTH_PASSWORD'))

app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return "Minha primeira API."

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to='en')
    polaridade = tb_en.sentiment.polarity
    return "polaridade: {}".format(polaridade)

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])

app.run(debug=True, host="0.0.0.0")