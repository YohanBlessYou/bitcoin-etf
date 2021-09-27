
from foundation import *
from account import *
from krw_balance import *
from market_info import *
from order import *
from observer import *

print("- sell_all")
print("- buy_etf")
print("- cancel_all_order")
print("- show_account")
print("- auto_seller")
# print("- etf_observer")
cmd = input("입력하세요 : ")

if cmd == "sell_all":
    sell_all()
elif cmd == "buy_etf":
    print("")
    print("1: 전체 자산")
    print("2: 남은 KRW")
    print("3: 금액지정")
    option = input("분배할 금액을 선택하세요 : ")
    buy_etf(option)
elif cmd == "cancel_all_order":
    cancel_all_order()
elif cmd == "show_account":
    show_total_my_account_info_with_print()
elif cmd == "auto_seller":
    auto_seller()
# elif cmd == "etf_observer":
#     auto_market_status_checker()
