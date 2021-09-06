
from foundation import *
from account import *
from krw_balance import *
from market_info import *
from order import *

print("- sell_all")
print("- buy_etf")
print("- cancel_all_order")
print("- show_account")

cmd = input("입력하세요 : ")

if cmd == "sell_all":
    sell_all()
elif cmd == "buy_etf":
    buy_etf()
elif cmd == "cancel_all_order":
    cancel_all_order()
elif cmd == "show_account":
    show_total_my_account_info_with_print()
