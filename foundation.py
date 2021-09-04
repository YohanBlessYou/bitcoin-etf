import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

from api_key import *

access_key = UPBIT_OPEN_API_ACCESS_KEY
secret_key = UPBIT_OPEN_API_SECRET_KEY
server_url = {
    "accounts": "https://api.upbit.com/v1/accounts",
    "market_list": "https://api.upbit.com/v1/market/all",
    "order_list": "https://api.upbit.com/v1/orders",
    "cancel_order": "https://api.upbit.com/v1/order",
    "current_price": "https://api.upbit.com/v1/ticker",
    "sell": "https://api.upbit.com/v1/orders",
    "buy": "https://api.upbit.com/v1/orders",
    "all_ticker_list": "https://api.upbit.com/v1/market/all",
}

def error_handling(res):
    res_json = res.json()
    if res.status_code == 200:
        return
    if res.status_code == 201:
        return
    if res.status_code == 400:
        print("")
        print("\033[31m"+"<<Error>> : " + res_json['error']['message'])
        print("\033[0m")
    elif res.status_code != 200:
        print("")
        print("\033[34m"+"<<" + str(res.status_code) + ">>")
        print("\033[0m")