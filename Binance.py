import pandas as pd
import numpy as np
from binance.spot import Spot
import configparser
import requests
import json


'''
API Doc
https://github.com/binance/binance-spot-api-docs/blob/master/rest-api_CN.md
'''

if __name__ == '__main__':
    # Restful API
    base_url = 'https://api.binance.com'    # json response / unix / ms
    response = requests.get('https://data-api.binance.vision/api/v3/exchangeInfo?symbol=BTCUSDT')
    if response.status_code == 200:
        data = response.json()  # Python dict
    else:
        print(f"Request Failed, Satus code: {response.status_code}")
    data_json = json.loads(response.text)


    # Function API
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    # api_key = config.get('keys', 'api_key')
    # api_secret = config.get('keys', 'api_secret')
    # print('DEBUG POINT HERE')
    #
    # client = Spot()
    # print(client.klines("BTCUSDT", '1m'))
    # # timeZone = 0 ---> UTC
    # data = client.klines(symbol='BTCUSDT', interval='1m', startTime=1499040000000, endTime=1599644799999, timeZone='0')
    # # print(client.klines("BNBUSDT", "1h", limit=10))
    # client = Spot(api_key=api_key, api_secret=api_secret)
    # print(client.account())
