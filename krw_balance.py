from foundation import *
from account import *

def find_my_cash_element(account_info):
    for element in account_info:
        if element['currency'] == 'KRW':
            return element

def get_my_available_cash():
    global avaliable_cash
    account_info = show_total_my_account_info()

    cash_info = find_my_cash_element(account_info)
    if cash_info == None:
        error_handling("get_available_cash()")
        return

    # consider transaction fee
    available_cash = int(float(cash_info['balance']) * 0.9995)

    return available_cash

