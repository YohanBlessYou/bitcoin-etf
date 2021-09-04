from foundation import *

def error_handling(function_name):
    print("something wrong in "+function_name)

def find_cash_element(account_info):
    for element in account_info:
        if element['currency'] == 'KRW':
            return element

def get_available_cash():
    global avaliable_cash
    account_info = show_total_account_info()

    cash_info = find_cash_element(account_info)
    if cash_info == None:
        error_handling("get_available_cash()")
        return

    return int(float(cash_info['balance']))

def show_total_account_info():
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

    print("")
    print("<현재 자산 리스트>")

    for coin in res_json:
        print("- "+coin['currency']+" : "
            +str(round(float(coin['balance']),0)))
    
    print("")

    return res_json