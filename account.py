from foundation import *
from market_info import *

def show_total_my_account_info():
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.get(server_url["accounts"], headers=headers)

    if res.status_code != 200:
        print("")
        print("\033[34m"+"<<" + res.status_code + ">>")
        print("\033[0m")

    res_json = res.json()

    return res_json

def show_total_my_account_info_with_print():
    res_json = show_total_my_account_info()

    print("")
    print("<현재 자산 리스트>")

    for coin in res_json:
        print("- "+coin['currency']+" : "
            +str(round(float(coin['balance']),0)))
    
    print("")

    return res_json



def get_my_order_list(order_type):
    query = {
        'state': order_type,
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
    res = requests.get(server_url["order_list"], params=query, headers=headers)
    return res.json()

def get_my_order_uuid_list():
    uuids = []
    
    res = get_my_order_list("watch")

    for element in res:
        uuids.append(element['uuid'])

    res = get_my_order_list("wait")

    for element in res:
        uuids.append(element['uuid'])

    return uuids


def get_dont_have_coin_list():

    coin_list_json = get_all_krw_coin_list()

    already_having_coin_list = show_total_my_account_info()

    buy_coin_list = []

    exist_flag = 0

    # remove coins having already from list
    for target_coin in coin_list_json:
        exist_flag = 0
        for having_coin in already_having_coin_list:
            if target_coin['market'] == "KRW-"+having_coin['currency']:
                exist_flag = 1
        if exist_flag == 0:
            buy_coin_list.append(target_coin)

    return buy_coin_list