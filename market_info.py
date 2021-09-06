from foundation import *
from time import sleep

def get_current_price(ticker):
    sleep(0.1)

    query = {
        'markets': ticker,
    }

    headers = {"Accept": "application/json"}

    res = requests.get(server_url["current_price"], params=query, headers=headers)

    res_json = res.json()

    error_handling(res)

    return res_json[0]['trade_price']


def get_all_krw_coin_list():
    querystring = {"isDetails":"false"}

    headers = {"Accept": "application/json"}

    res = requests.get(server_url["all_ticker_list"], headers=headers, params=querystring)

    res_json = res.json()

    coin_list = []

    for coin in res_json:
        if coin['market'].startswith('KRW'):
            coin_list.append(coin)


    return coin_list