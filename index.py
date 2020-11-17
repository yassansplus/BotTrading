
import requests
import time
import hmac
import hashlib
import json
import base64
import urllib
import os

Kraken_secret_key = 'pp1SpnXvn4Wr+chbXWG/baFzFvLJCDPNpp/XfTZJWsrUGJS8Wp79BDIkug8iALp5k42TukpgTcgSp3OGZbxnJA=='
Kraken_headers = {'API-Key': 'EB2e94jAdKzEPjIAsAxTfPUl7vuvKfN4+8jUiBtn6MxD1rvAG8srtUZW'
}
Kraken_nonce = str(int(time.time()*1000))
Kraken_POST_data = {'nonce': Kraken_nonce}


def Kraken_account_balance(Kraken_headers, URI_path):

    URL_path = 'https://api.kraken.com'+URI_path
    
    url_encoded_post_data = urllib.parse.urlencode(Kraken_POST_data)
    encoded = (str(Kraken_POST_data['nonce'])+url_encoded_post_data).encode()
    message = URI_path.encode() + hashlib.sha256(encoded).digest()

    Kraken_signature = hmac.new(base64.b64decode(Kraken_secret_key), message, hashlib.sha512)
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
    return result['result']


def Kraken_All_Pairs(Kraken_headers, URI_path):

    URL_path = 'https://api.kraken.com' + URI_path
    response = requests.post(
        URL_path, data=Kraken_POST_data, headers=Kraken_headers)

    result = response.json()
    Save_Data_Into_File(list(result['result'].keys()), 'pairs.json')
    return result['result']


def Kraken_Pair(Kraken_headers, URI_path, pair):

    URL_path = 'https://api.kraken.com'+URI_path
    Kraken_POST_data['pair'] = pair
    response = requests.post(
        URL_path, data=Kraken_POST_data, headers=Kraken_headers)

    result = response.json()
    return result['result']

def Save_Data_Into_File(content, filename):
    if os.stat(filename).st_size == 0:
        f= open(filename,"w+")
        with f as file:
            file.write(json.dumps(content))
        f.close
    
        


#krakenBalance = Kraken_account_balance(Kraken_headers, '/0/private/Balance')# On recupere un object avec tout nos currency

#Kraken_server_Time = Kraken_server_Time(Kraken_headers,'/0/public/Time') # On recupere un objet avec notre server
Kraken_All_Pairs = Kraken_All_Pairs(Kraken_headers, '/0/public/AssetPairs')  # On recupere toutes les pairs

#Kraken_Pair = Kraken_Pair(Kraken_headers,'/0/public/Ticker', 'LTCEUR')  # On recupere une pair



