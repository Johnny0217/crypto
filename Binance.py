import pandas as pd
import numpy as np
from binance.spot import Spot
import configparser

'''
https://github.com/binance/binance-connector-python
'''

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config.get('keys', 'api_key')
    api_secret = config.get('keys', 'api_secret')
    print('DEBUG POINT HERE')

    client = Spot()
    print(client.klines("BTCUSDT", '1m'))
    client = Spot(api_key=api_key, api_secret=api_secret)
    print(client.account())
