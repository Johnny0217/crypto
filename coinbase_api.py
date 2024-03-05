# -*- coding: utf-8 -*-
'''
@Time : 2024/3/5 13:59
@Author : Jun
'''
import http.client
import json
from urllib.parse import urlunparse
import urllib.parse
import requests
import pandas as pd
import os
from utils import mk_data_path_from_vary_source, log_info

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
