from foundation import *
from account import *
from krw_balance import *
from market_info import *
from time import sleep

def cancel_all_order():
    orders = get_my_order_uuid_list()
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
    account_json = show_total_my_account_info_with_print()

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
    sleep(1)

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

        error_handling_with_query(res, query)


def get_converted_order_list_for_buy():

    coin_list_json = get_dont_have_coin_list()

    my_total_cash = get_my_available_cash()
    cash_for_each = int(my_total_cash/len(coin_list_json))

    print("")
    print("\033[32m")
    print("현재 KRW 잔고 : "+str(my_total_cash)+"원")
    print("각 : "+str(cash_for_each)+"원")
    print("구매 코인 수 : "+str(len(coin_list_json))+"개")
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
    sleep(1)

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

        error_handling_with_query(res, query)

    print("구매가 완료되었습니다")