from binance.client import Client
import datetime
from prettytable import PrettyTable
import matplotlib

api_key = "c5gv7l2eFdoqQU0ZBLO20ZnsWcO5EfrRigxAGfUrcHWgUQV5PZ9UkDWXAcLRFbwt"
api_secret = "1XqRTjU5Hg70Xhr7KaTLYAYnPDSBNIQP5lgolU6QhK04zdOjl8zLEao93Fj7EY3i"
client = Client(api_key,api_secret)

CEND = '\033[0m'
CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'
tradesTable = PrettyTable()
tradesTable.field_names = ['PAIR','DATE','PRICE','AMOUNT']
dataTable = PrettyTable()
dataTable.field_names = ['PAIR','PRICE','TIME FRAME','TRADES','BUY','SELL','TOTAL','DIFFERENCE','BUY %' ,'SELL %','BUY/SELL %']
#PAIR = 'RCNBTC'
PAIR = input('>Enter the pair ex_(RCNBTC) : ')
timeFrame = input('>Enter the time frame in minutes : ')
#timeFrame = '30'
agg_trades = client.aggregate_trade_iter(symbol=PAIR, start_str= timeFrame+' minutes ago UTC')
symbolPrice = client.get_symbol_ticker(symbol = PAIR)
price = symbolPrice['price']

trades = 0
sell = 0
buy = 0
buyMoyPrice = 0
sellMoyPrice = 0
buyTrades = 0
sellTrades = 0

for trade in agg_trades:
    #print(datetime.datetime.fromtimestamp(trade['T']/1000))
    if(trade['m']):
        action = CRED
        sell = sell + float(trade['q'])
        buyMoyPrice = buyMoyPrice + float(trade['p'])
        buyTrades = buyTrades + 1
    else:
        action = CGREEN
        buy = buy + float(trade['q'])
        sellMoyPrice = sellMoyPrice + float(trade['p'])
        sellTrades = sellTrades + 1

    price = action + trade['p']+CEND
    trades = trades + 1


    tradesTable.add_row([PAIR,datetime.datetime.fromtimestamp(trade['T']/1000),price,trade['q']])


rate  = (( buy / sell ) * 100 ) - 100
if rate < 0:
    rate = CRED + format(rate,'.2f') + '%' + CEND
else:
    rate = CGREEN + format(rate,'.2f') + '%' + CEND

total = buy + sell
buyPercent = CGREEN + format( ( buy * 100 ) / total , '.2f') + '%' + CEND
sellPercent = CRED + format( ( sell * 100 ) / total , '.2f') + '%' + CEND
difference = buy - sell
buy = CGREEN + str(buy) + CEND
sell = CRED + str(sell) + CEND
sellMoyPrice = CRED + format(sellMoyPrice / sellTrades,'.10f') + CEND
buyMoyPrice = CGREEN + format( buyMoyPrice / buyTrades,'.10f') + CEND



if difference < 0 :
    difference = CRED + str(difference) + CEND
else:
    difference = CGREEN + str(difference) + CEND

dataTable.add_row([PAIR,price,' last 30 MIN ',trades,buy,sell,total,difference,buyPercent,sellPercent,rate])

print(tradesTable)
print(dataTable)

