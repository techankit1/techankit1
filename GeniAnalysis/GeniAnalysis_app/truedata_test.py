from truedata_ws.websocket.TD import TD
from copy import deepcopy
import time
import logging
from datetime import datetime as dt

td_obj = TD('tdws199', 'ashish@199_stockgini', live_port=8084 , log_level= logging.WARNING )

symbols = ['NIFTY 50', 'NIFTY BANK', 'NIFTY-I', 'INDIA VIX']
req_ids = td_obj.start_live_data(symbols)
live_data_objs = {}
time.sleep(1)

nifty_chain = td_obj.start_option_chain('NIFTY', dt(2022 , 3 , 3), chain_length = 10, bid_ask = True)
time.sleep(2)

for req_id in req_ids:
    print(td_obj.touchline_data[req_id])

print(nifty_chain.get_option_chain())

