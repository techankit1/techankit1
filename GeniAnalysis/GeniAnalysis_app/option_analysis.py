"""

from truedata_ws.websocket.TD import TD
from copy import deepcopy
import time
import logging
from datetime import datetime as dt
import pandas as pd
pd.set_option("display.max_columns", None, "display.max_rows", None)
username = 'tdws186'

password = 'ashish@186_x'

td_obj = TD(username, password, live_port=8082, log_level= logging.WARNING)
# td_obj = TD(username, password, log_level= logging.WARNING)

symbols = ['NIFTY 50']
# starting live data for symbols 
req_ids = td_obj.start_live_data(symbols)
live_data_objs = {}
time.sleep(1)

# initilizing option chain with symbol expiry chain length(optional) , bid ask (optional)
nifty_chain = td_obj.start_option_chain( 'NIFTY', dt(2022, 1, 27), chain_length = 22, bid_ask = False)
# nifty_chain = td_obj.start_option_chain( 'BANKNIFTY', dt(2022 , 1 , 27), chain_length = 10, bid_ask = True)

# td_app.disconnect()
 
time.sleep(2)



# while True:
    # print(nifty_chain.get_option_chain())
    # time.sleep(5)


for req_id in req_ids:
    live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])
    
print(nifty_chain.get_option_chain())

count = 1
while True:
    for req_id in req_ids:
        if not td_obj.live_data[req_id] == live_data_objs[req_id]:
            print( f'{td_obj.live_data[req_id].symbol} ==> {td_obj.live_data[req_id].ltp}')
            live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])            
            if count % 50 == 0:
                print(nifty_chain.get_option_chain())
            count += 1
    time.sleep(0.05)  ## important otherwise cpu will overthrottle.
		
		
"""