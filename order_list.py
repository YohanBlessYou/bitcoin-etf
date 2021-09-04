from foundation import *

def get_order_list(order_type):
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

def get_order_uuid_list():
    uuids = []
    
    res = get_order_list("watch")

    for element in res:
        uuids.append(element['uuid'])

    res = get_order_list("wait")

    for element in res:
        uuids.append(element['uuid'])

    return uuids


def get_all_krw_coin_list():
    querystring = {"isDetails":"false"}

    headers = {"Accept": "application/json"}

    res = requests.get(server_url["all_ticker_list"], headers=headers, params=querystring)

    res_json = res.json()

    coin_list = []

    for coin in res_json:
        if coin['market'].startswith('KRW'):
            coin_list.append(coin)

    print("")
    print("\033[32m"+"총 " + str(len(coin_list)) + "개의 코인을 구매합니다")
    print("\033[0m")

    return coin_list


