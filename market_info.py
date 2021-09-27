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


# def get_flow_volume_from_coin(ticker):
#     coin_list = get_all_krw_coin_list()
#     url = "https://api.upbit.com/v1/candles/minutes/5"

#     querystring = {
#         "market":ticker,
#         "count":"3"
#     }

#     headers = {"Accept": "application/json"}

#     response = requests.request("GET", url, headers=headers, params=querystring)

#     print(response.text)


# def get_etf_profit(time, ticker):



# def get_average_etf_profit(time):
#     coin_list = get_all_krw_coin_list()

#     sum = 0

#     for coin in coin_list:
#         sum += get_etf_profit(coin['market'])
    
# def print_etf_profit_rate_timetable():
    
#     print(get_average_etf_profit(0))
    