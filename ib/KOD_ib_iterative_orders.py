#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 14:02:09 2020

@author: kieranodonnell
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:20:32 2020

@author: kieranodonnell
"""

# IB API Client & Wrapper Classes

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order


#Asynch implementation with multithreading
import threading
import time

class TradingApp(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self,self)
                
    def nextValidId(self, orderId: int): # This function generates a subsequent valid orderId 
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)
        
def websocket_con():
    app.run() # start connection, is persistent, so needs to be closed!!
    
app = TradingApp() # Instantiate class (self defined)
app.connect("127.0.0.1", 7497 , clientId=1) #Establish websocket connection

connection_thread = threading.Thread(target=websocket_con, daemon=True) # pass app.run
connection_thread.start()
time.sleep(1) # make a lag


# Contract generation
def usTechStk(symbol, secType="STK", currency ="USD", exchange="ISLAND"):
    contract = Contract() 
    contract.symbol = symbol
    contract.secType = secType
    contract.currency = currency
    contract.exchange = exchange
    return contract
    
def limitOrder(direction, quantity, lmt_price):
    order = Order()
    order.action = direction
    order.orderType = "LMT"
    order.totalQuantity = quantity
    order.lmtPrice = lmt_price
    return order

order_id = app.nextValidOrderId
app.placeOrder(order_id, usTechStk("FB"), limitOrder("BUY",1,10)) #connect contracts to app
time.sleep(5)
app.cancelOrder(order_id)

app.reqIds(-1)
time.sleep(3) # insert lag
order_id = app.nextValidOrderId

app.placeOrder(order_id, usTechStk("FB"), limitOrder("BUY",1,19)) #connect contracts to app
time.sleep(3)

app.cancelOrder(order_id)
time.sleep(5) # close daemon thread!