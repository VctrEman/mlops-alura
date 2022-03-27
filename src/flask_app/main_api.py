# https://www.youtube.com/watch?v=DJn7X0QZ0qQ
# set up venv on vscode #https://techinscribed.com/python-virtual-environment-in-vscode/

#Import Flask modules
from flask import Flask, request, jsonify
from textblob import TextBlob

import pandas as pd
import os
from flask_basicauth import BasicAuth
import pickle
from sklearn.linear_model import LinearRegression

#start from ml_ops go to flask_app
#os.chdir('src/flask_app')

colunas = ['tamanho','ano','garagem']
#modelo = pickle.load(open(os.path.join(mydir, myfile),"rb"))
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in CWD %r: %s" % (cwd, files))

modelo = pickle.load(open("../../models/modelo.sav","rb"))
#modelo = pickle.load(open("models/modelo.sav","rb"))

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return "My first API"

# Pass the required route to the decorator.
@app.route("/hello")
@basic_auth.required   #teste auth
def hello():
    return "Hello, Welcome to my first API"

@app.route('/sentimento<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to='en')
    return "polaridade: {}".format(tb_en.sentiment.polarity)


@app.route('/cotacao/',methods=['POST']) #receives a list with json objects
def cotacao():
    dados = request.get_json() #returns a list of dicts
    #dados_input = [dados[col] for col in colunas]
    preco = modelo.predict( pd.DataFrame.from_dict( dados ) ).tolist()
    return jsonify(preco=preco)


app.run(debug=True) #debug = true allows syncronous tests, in other words debugging

print(1)
