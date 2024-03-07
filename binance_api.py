# -*- coding: utf-8 -*-
'''
@Time : 2024/3/5 13:59
@Author : Jun
'''

import pandas as pd
import numpy as np
from binance.spot import Spot
import configparser
import requests
import json
from utils import *
from urllib.parse import urlunparse, urlencode
import urllib.parse
from datetime import datetime
import time
import pytz

'''
API Doc
https://github.com/binance/binance-spot-api-docs/blob/master/rest-api_CN.md
all response from public binance RESTful API -> json format
[a1, a2, a3, ...] -> a1 represents the earliest time
UNIX time -> ms

kline interval
1s 1m 3m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w 1M
'''


def check_connection():
    scheme = "https"
    net_loc = 'api.binance.com'
    path = '/api/v3/ping'
    url = urlunparse((scheme, net_loc, path, '', '', ''))
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Python dict
        print(f'{log_info()} connection is good!')
    else:
        print(f"{log_info()} Request Failed, Satus code: {response.status_code}")


def get_ob_depth(symbol: str, limit: int = 10):
    ''' GET /api/v3/depth
    limit       weight
    1-100       5
    101-500     25
    501-1000    50      limit by default = 100 max 5000 [5, 10, 20, 50, 100, 500, 1000, 5000]
    1001-5000   250     limit = 100 -> returns all order book (extremely large volume of data)
    '''
    scheme = "https"
    net_loc = 'api.binance.com'
    path = '/api/v3/depth'
    query_params = urlencode({'symbol': f'{symbol}', 'limit': f'{limit}'})
    url = urlunparse((scheme, net_loc, path, '', query_params, ''))
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Python dict
        data = pd.DataFrame(data).sort_values(by=['lastUpdateId'])
        return data
    else:
        print(f"{log_info()} Request Failed, Satus code: {response.status_code}")


def get_aggTrades(symbol: str, startTime: int = None, endTime: int = None, limit: int = 1000, fromId: int = None):
    '''
    :param symbol: BTCUSDT / ETHUSDT
    :param startTime: unix ms
    :param endTime: unix ms
    :param limit: max 1000
    :param fromId: not used
    '''
    scheme = "https"
    net_loc = 'api.binance.com'
    path = '/api/v3/aggTrades'
    query_params = {'symbol': f'{symbol}', 'limit': f'{limit}'}
    if startTime is not None:
        query_params['startTime'] = f'{startTime}'
        query_params['endTime'] = f'{endTime}'
    if fromId is not None:
        query_params['fromId'] = f'{fromId}'
    query = urlencode(query_params)
    url = urlunparse((scheme, net_loc, path, '', query, ''))
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if type(data) == list:
            if len(data) == 0:
                print('Request response is empty')
                return
            else:
                data = pd.DataFrame(data)
                data['datetime_utc'] = pd.to_datetime(data['T'], unit='ms')
                bj_tz = pytz.timezone('Asia/Shanghai')
                data['datetime_bj'] = data['datetime_utc'].dt.tz_localize('UTC').dt.tz_convert(bj_tz)
                data = data.sort_values(by=['datetime_bj'])
                return data
    else:
        print(f"{log_info()} Request Failed, Satus code: {response.status_code}")


if __name__ == '__main__':
    # check_connection()
    # ob_data = get_ob_depth('BTCUSDT', 100)
    start = beijing_datetime_to_unix('2017-09-01 08:01:00')
    end = beijing_datetime_to_unix('2017-09-01 08:02:00')
    # start = beijing_datetime_to_unix('2023-12-11 00:01:00')
    # end = beijing_datetime_to_unix('2023-12-11 00:02:00')
    # save_path = mk_data_path_from_vary_source('binance')
    # startTime - endTime
    # df = get_aggTrades('BTCUSDT', start, end, limit=1000)
    # fromId test
    # df = get_aggTrades('BTCUSDT', limit=1000, fromId=61458)
    print('DEBUG POOINT HERE')
    # df.to_csv(f'{save_path}/1min_aggTrades.csv')
