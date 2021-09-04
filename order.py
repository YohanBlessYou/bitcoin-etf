from foundation import *
from order_list import *
from cash_info import *
from market_price import *
from time import sleep

def cancel_all_order():
    orders = get_order_uuid_list()
    for order in orders:
        query = {
            'uuid': order,
        }
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.delete(server_url["cancel_order"], params=query, headers=headers)

        res_json = res.json()

        error_handling(res)


def get_converted_order_list_for_sell():
    account_json = show_total_account_info()

    ticker_list = []

    for currency in account_json:
        if currency['currency'] == 'KRW':
            continue
        if currency['unit_currency'] == 'KRW':
            query = {
                'market': "KRW-" + currency['currency'],
                'volume': currency['balance'],
                'price': get_current_price("KRW-" + currency['currency']),
            }
            ticker_list.append(query)

    return ticker_list

def sell_all():

    cancel_all_order()

    order_list = get_converted_order_list_for_sell()

    for coin in order_list:
        sleep(0.2)
        query = {
            'market': coin['market'],
            'side': 'ask',
            'volume': coin['volume'],
            'price': coin['price'],
            'ord_type': 'limit',
        }

        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.post(server_url['sell'], params=query, headers=headers)

        res_json = res.json()

        error_handling(res)


def get_converted_order_list_for_buy():
    coin_list_json = get_all_krw_coin_list()

    temp_coin_list_json = coin_list_json
    already_having_coin_list = show_total_account_info()

    # remove coins having already from list
    for target_coin in coin_list_json:
        for having_coin in already_having_coin_list:
            if target_coin['market'] == "KRW-"+having_coin['currency']:
                temp_coin_list_json.remove(target_coin)
    
    coin_list_json = temp_coin_list_json

    my_total_cash = get_available_cash()
    cash_for_each = int(my_total_cash/len(coin_list_json))

    print("")
    print("\033[32m")
    print("total : "+str(my_total_cash))
    print("각 : "+str(cash_for_each))
    print("코인 수 : "+str(len(coin_list_json)))
    print("\033[0m")

    ticker_list = []

    for target_coin in coin_list_json:
        current_price = get_current_price(target_coin['market'])
        volume_per_coin = round(cash_for_each/current_price, 7)

        query = {
            'market': target_coin['market'],
            'volume': volume_per_coin,
            'price': current_price,
        }
        ticker_list.append(query)

    return ticker_list


def buy_etf():

    cancel_all_order()

    order_list = get_converted_order_list_for_buy()

    for coin in order_list:
        sleep(0.2)
        query = {
            'market': coin['market'],
            'side': 'bid',
            'volume': coin['volume'],
            'price': coin['price'],
            'ord_type': 'limit',
        }

        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.post(server_url['buy'], params=query, headers=headers)

        res_json = res.json()

        error_handling(res)

    print("구매가 완료되었습니다")