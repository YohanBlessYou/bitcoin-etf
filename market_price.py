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


