
from account import *
from order import *


def auto_seller():
    high_amount = int(input("상한가를 입력하세요 : "))
    low_amount = int(input("하한가를 입력하세요 : "))
    while True:
        current_account_info = get_my_total_current_amount()
        if current_account_info < low_amount:
            print("WTF")
            print(current_account_info)
            sell_all()
            sleep(10)
            sell_all()
            sleep(10)
            sell_all()
            break
        if current_account_info > high_amount:
            print("so good")
            print(current_account_info)
            sell_all()
            sleep(10)
            sell_all()
            sleep(10)
            sell_all()
            break
        sleep(10)
        print(current_account_info)


def auto_market_status_checker():
    print(get_flow_volume_from_coin("KRW-BTC"))