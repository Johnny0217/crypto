# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 09:34:10 2020

@author: Dell
"""

"""
ref:
https://github.com/ramoslin02/51bitqunt/blob/master/binance_api/binance.py   
"""

import requests
import time
from datetime import datetime
import datetime as dt
import pandas as pd
from multiprocessing import Pool
import os
from sym import lst_api_syms, lst_fapi_syms, lst_all_syms

pd.set_option('expand_frame_repr', False)


def download_singleday_marketdata_from_binanceAPI(in_):
    """
    download singleday marketdata by given symbol, interval and etc
    """
    BASE_URL = 'https://api.binance.com'
    kline = '/api/v1/klines'

    symbol = in_[0]
    interval = in_[1]
    start_day = in_[2]
    save_path = in_[3]
    if "m" in interval:
        mins = int(interval.split("m")[0])
    elif "h" in interval:
        mins = int(interval.split("h")[0]) * 60
    elif "d" in interval:
        mins = int(interval.split("d")[0]) * 60 * 24

    limit = max(1, min(1000, 60 * 24 // mins - 1))
    start_time0 = int(time.mktime(start_day.timetuple())) * 1000
    end_time0 = int(time.mktime((start_day + dt.timedelta(1)).timetuple())) * 1000 - 60 * 1000
    df_lst = []
    start_time = start_time0
    day_delta = limit * mins * 60 * 1000
    end_time = start_time + day_delta
    print("symbol: %s,  interval: %s,  start_day: %s" % (symbol, interval, start_day))
    while True:
        url = BASE_URL + kline + \
              '?symbol=%s&interval=%s&limit=%s' % (symbol, interval, limit) + \
              '&startTime=%s' % str(start_time) + \
              '&endTime=%s' % str(end_time)
        resp = requests.get(url)
        data = resp.json()

        tmp_df = pd.DataFrame(data, columns={'open_time_unix': 0, 'open': 1, 'high': 2, 'low': 3,
                                             'close': 4, 'volume': 5, 'close_time_unix': 6, 'quote_volume': 7,
                                             'trades': 8, 'taker_base_volue': 9,
                                             'taker_quote_volume': 10, 'ignore': 11})
        if len(tmp_df) == 0:
            return
        tmp_df.set_index('open_time_unix', inplace=True, drop=False)
        df_lst.append(tmp_df)
        if end_time >= end_time0:
            break
        start_time = end_time
        end_time = min(end_time0, start_time + day_delta)

    df = pd.concat(df_lst, axis=0)
    df.drop_duplicates(inplace=True)

    df.index = pd.to_datetime(df.index, unit='ms')
    df.index = df.index.tz_localize('UTC')
    df.index = df.index.tz_convert('Asia/Shanghai')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    df.to_csv(os.path.join(save_path, start_day.strftime('%Y%m%d') + '.csv'), index_label='DateTime')

    return


def get_date_list(start, end):
    """
    get date list between start and end
    start, end:  in datetime.datetime
    return: string
    """
    date_list = []
    date = start
    while date <= end:
        date_list.append(date)
        date = date + dt.timedelta(1)

    return date_list


def download_marketdata_from_binanceAPI(symbol, start_, end_, interval, root_path, workers=2):
    """
    download mins data
    """
    dic_interval = {'1d': '1day', '1h': '1hour', '1m': '1min'}
    save_path = os.path.join(root_path, dic_interval[interval], symbol)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    # load current date list saved data
    sv_date_lst = os.listdir(save_path)
    if len(sv_date_lst) != 0:
        sv_date_lst = [x.split(".csv")[0] for x in sv_date_lst]
        sv_date_lst = [dt.datetime(int(x[:4]), int(x[4:6]), int(x[6:])) for x in sv_date_lst]
    # make date list
    start_date = dt.datetime(int(start_[0]), int(start_[1]), int(start_[2]))
    end_date = dt.datetime(int(end_[0]), int(end_[1]), int(end_[2]))
    date_lst = get_date_list(start_date, end_date)
    # remove the date list already download
    date_lst = [x for x in date_lst if x not in sv_date_lst]
    count = len(date_lst)

    in_lst = [x for x in zip([symbol] * count, [interval] * count, date_lst, [save_path] * count)]
    if workers == '':
        for in_ in in_lst:
            download_singleday_marketdata_from_binanceAPI(in_)
            # time.sleep(0.02)
    else:
        pool = Pool(workers)
        res_lst = pool.map(download_singleday_marketdata_from_binanceAPI, in_lst)

    return


symbol_lst = ['ADAUSDT', 'BCHUSDT', 'BNBUSDT', 'BTCUSDT', 'DASHUSDT',
              'EOSUSDT', 'ETCUSDT', 'ETHUSDT', 'LINKUSDT', 'LTCUSDT',
              'NEOUSDT', 'TRXUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT',
              'XTZUSDT', 'ZECUSDT']
filters = []
symbol_lst = [x for x in lst_api_syms if x not in filters]

if __name__ == "__main__":

    ###download daily spot data from Binance from yesterday_1 to yesterday, all period days
    ###the code is based on VPN
    period = 1
    today_str = dt.datetime.now().date().strftime("%Y%m%d")
    today = dt.datetime.now()
    yesterday = today - dt.timedelta(1)
    yesterday_1 = today - dt.timedelta(period)
    today_str = today.date().strftime("%Y%m%d")
    yesterday_str = yesterday.date().strftime("%Y%m%d")
    yesterday_1_str = yesterday_1.date().strftime("%Y%m%d")
    for symbol_ in symbol_lst:
        download_marketdata_from_binanceAPI(symbol=symbol_,
                                            start_=[yesterday_1_str[:4], yesterday_1_str[4:6], yesterday_1_str[6:]],
                                            end_=[yesterday_str[:4], yesterday_str[4:6], yesterday_str[6:]],
                                            interval='1d',
                                            root_path='/home/quant/crypto/data/Binance/spot/',
                                            workers='')
