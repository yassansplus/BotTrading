
import requests
import time
import hmac
import hashlib
import json
import base64
import urllib
import os
from os import listdir
from os.path import isfile, join
from statistics import mean 
import decimal
decimal.getcontext().prec = 30
Kraken_secret_key = 'h7N/0rOXbGU0xFrhR6aufEHaWH2lFBWA7aW+j2AOqmzivaotk2oOpnhR+jTP385pK50YY2dF+Np5nRqHb8o0iA=='
Kraken_headers = {'API-Key': '6hEJvDCceeQeibI1W8CnlC2j9otZxtsgWeM/pann9JGU4OoG1WH1azc8'
                  }
Kraken_nonce = str(int(time.time()*1000))
Kraken_POST_data = {'nonce': Kraken_nonce}

# fonction qui permet de recuperer les données de ce que l'on possède sur la plateforme


def Kraken_account_balance(Kraken_headers, URI_path):

    URL_path = 'https://api.kraken.com'+URI_path

    url_encoded_post_data = urllib.parse.urlencode(Kraken_POST_data)
    encoded = (str(Kraken_POST_data['nonce'])+url_encoded_post_data).encode()
    message = URI_path.encode() + hashlib.sha256(encoded).digest()

    Kraken_signature = hmac.new(base64.b64decode(
        Kraken_secret_key), message, hashlib.sha512)
    Kraken_signature_digest = base64.b64encode(Kraken_signature.digest())

    Kraken_headers['API-Sign'] = Kraken_signature_digest.decode()

    response = requests.post(
        URL_path, data=Kraken_POST_data, headers=Kraken_headers)

    result = response.json()

    return result['result']

# permet de recuperer le serverTime

def getPosition(Kraken_headers, URI_path):
    URL_path = 'https://api.kraken.com'+URI_path
    url_encoded_post_data = urllib.parse.urlencode(Kraken_POST_data)
    encoded = (str(Kraken_POST_data['nonce'])+url_encoded_post_data).encode()
    message = URI_path.encode() + hashlib.sha256(encoded).digest()

    Kraken_signature = hmac.new(base64.b64decode(
        Kraken_secret_key), message, hashlib.sha512)
    Kraken_signature_digest = base64.b64encode(Kraken_signature.digest())

    Kraken_headers['API-Sign'] = Kraken_signature_digest.decode()

    response = requests.post(
        URL_path, data=Kraken_POST_data, headers=Kraken_headers)

    result = response.json()
    return result['result']
    
def Kraken_server_Time(Kraken_headers, URI_path):

    URL_path = 'https://api.kraken.com'+URI_path

    response = requests.post(
        URL_path, data=Kraken_POST_data, headers=Kraken_headers)

    result = response.json()
    return result['result']["unixtime"]

# Permet de recuperer une liste de tout les paires


def Kraken_All_Pairs(Kraken_headers, URI_path):

    URL_path = 'https://api.kraken.com' + URI_path
    response = requests.post(
        URL_path, data=Kraken_POST_data, headers=Kraken_headers)

    result = response.json()
    # On envoie une list de ce qui doit etre enregistrer dans le fichier pairs.json -> donc tout nos paires possible.
    #Save_Data_Into_File(list(result['result'].keys()), 'pairs.json')
    return result['result']

# Fonction qui permet de recuperer les pairs souhaité


def Kraken_Pair(Kraken_headers, URI_path):

    dateTrade = Kraken_server_Time(Kraken_headers, '/0/public/Time')
      #regarder Ledger
    URL_path = 'https://api.kraken.com'+URI_path

    Kraken_POST_data['pair'] = ','.join(
        map(str, Kraken_All_Pairs(Kraken_headers, '/0/public/AssetPairs').keys()))
    response = requests.post(
        URL_path, data=Kraken_POST_data, headers=Kraken_headers)

    result = response.json()
    trade = {
        'currency' : result['result'],
    }
  
    numberOfTickersFile = len(os.listdir('Tickers'))
    print(numberOfTickersFile)
    file_saved = Save_Data_Into_File(trade, 'Tickers/'+str(numberOfTickersFile)+'_'+str(dateTrade)+'_Ticker.json')
    if file_saved:
        print('enregistrement du json avec Succes')
        return result['result']
    print('Il semblerait qu\'une erreur se soit produite')

# cette fonction permet d'enregistrer tout ce que l'on souhaite, il suffit de lui envoyer une list en entrer et elle enregistrera les clés. le deuxieme paragraphe et le filename


def Save_Data_Into_File(content, filename):
    print('Début de l\'enregistrement du fichier')
    with open(filename, "a+") as myfile:
        strJSON = json.dumps(content)        
        if os.path.getsize(filename) != 0:
            myfile.write(','+strJSON)
        else: 
            myfile.write(strJSON)
        print('fichier enregistré avec succès')
        myfile.close()
        return True
    return False

def getPriceHistory(pair):
    print('récuperation de la moyenne')
    search_dir = os.path.dirname(os.path.abspath(__file__))+'/Tickers'
    os.chdir(search_dir)
    tickers = filter(os.path.isfile, os.listdir(search_dir))
    tickers = [os.path.join(search_dir, f) for f in tickers] # add path to each file
    tickers.sort(key=lambda x: os.path.getmtime(x))
    pairPrice = []
    for ticker in tickers:
        with open(ticker, 'r') as f:
            number = ticker.split('_')[0]
            textJson = f.read()
            jsonParsed = json.loads(textJson)
            pairPrice.append(decimal.Decimal(jsonParsed['currency'][pair]['a'][0]))
            f.close()
    
    setMoyenne(pairPrice, pair)
    
def setMoyenne(pairPrice,pair):
    avg = sum(pairPrice) / len(pairPrice)
    filename = '../Moyenne/'+pair+'.csv'
    with open(filename, "a+") as myfile:
        myfile.write(str(avg)+';')
        myfile.close()
    print('La moyenne a été ajoutée.')
        




###################### Test des fonctions  ##################################

# krakenBalance = Kraken_account_balance(Kraken_headers, '/0/private/Balance')# On recupere un object avec tout nos currency

# On recupere un objet avec notre server

# Kraken_All_Pairs = Kraken_All_Pairs(Kraken_headers, '/0/public/AssetPairs')  # On recupere toutes les pairs



Kraken_Pair = Kraken_Pair(Kraken_headers, '/0/public/Ticker')  # On recupere une pair
Kraken_Pair

getPriceHistory('XBTCHF')

#getPosition(Kraken_headers, '/0/private/OpenPositions')


#A faire, recuperer dans le ledger, verifier s'il y a un ordre 
