# -*- coding: utf-8 -*-
'''
@Time : 2024/3/5 13:59
@Author : Jun
'''
import http.client
import requests
import pandas as pd
import os
import numpy as np
import requests
import json
from utils import *
from urllib.parse import urlunparse, urlencode
import datetime
from datetime import datetime, timedelta

'''
start
end
granularity {60, 300, 900, 3600, 21600, 86400} {1m, 5m, 15m, 1h, 6h, 1d}
max candles return = 300
'''


def get_all_known_trading_pairs_coinbase():
    ''' https://api.exchange.coinbase.com/products
    get a list of available currency pairs for trading
    :return:
    '''
    scheme = "https"
    netloc = "api.exchange.coinbase.com"
    path = "/products"
    url = urlunparse((scheme, netloc, path, '', '', ''))
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Python dict
        data_df = pd.DataFrame(data)
        data_df = data_df.sort_values(by=['id'])
        return data_df
    else:
        print(f"Request Failed, Satus code: {response.status_code}")


if __name__ == '__main__':
    # save_path exists under current project
    save_path = mk_data_path_from_vary_source('coinbase')
    trading_pairs = get_all_known_trading_pairs_coinbase()
    print('DEBUG POINT HERE')
    symbol = 'BTC-USDT'
    start_bj = '2024-01-01 08:00:00'
    end_bj = '2024-03-07 08:00:00'
    start = int(beijing_datetime_to_unix(start_bj) / 1000)
    end = int(beijing_datetime_to_unix(end_bj) / 1000)
    url = f'https://api.exchange.coinbase.com/products/{symbol}/candles/?start={start}&end={end}&granularity=86400'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    data.columns = ['unix_s', 'low', 'high', 'open', 'close', 'volume']
    data['UTC_datetime'] = data['unix_s'].apply(lambda x: datetime.utcfromtimestamp(x))
    data['Beijing_datetime'] = data['UTC_datetime'].apply(lambda x: x + timedelta(hours=8))
    print(f'{start_bj[:10]}_{end_bj[:10]} saved')
    data.to_csv(f'{symbol}_{start_bj[:10]}_{end_bj[:10]}.csv')
    print('DEBUG POINT HERE')
