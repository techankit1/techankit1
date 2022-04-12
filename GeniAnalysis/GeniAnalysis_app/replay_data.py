# from truedata_ws.websocket.TD import TD
# import time
# import logging
# from copy import deepcopy


# username = 'tdws199'
# password = 'ashish@199_stockgini'

# realtime_port = 8084


# url = 'replay.truedata.in'

# symbols = ['NIFTY 50']

# td_obj = TD(username, password, live_port=realtime_port, url=url, log_level=logging.DEBUG, log_format="%(message)s")

# print('\nStarting Real Time Feed.... ')

# req_ids = td_obj.start_live_data(symbols)
# live_data_objs = {}

# time.sleep(1)

# for req_id in req_ids:
    # live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])

# while True:
    # for req_id in req_ids:
        # if not td_obj.live_data[req_id] == live_data_objs[req_id]:
            # print(f'{td_obj.live_data[req_id].symbol} > {td_obj.live_data[req_id].ltp} > {td_obj.live_data[req_id].change:.2f}')
            # live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])
            
            

from truedata_ws.websocket.TD import TD
import time
import logging
from copy import deepcopy


# username = 'tdws199'
# password = 'ashish@199_stockgini'

username = 'tdws186'
password = 'ashish@186_stockgini'

realtime_port = 8082
# url = 'push.truedata.in'
# Disable the Production url above and Enable the Replay url below, when you need to work with the replay feed
# Make sure to re-enable the Production url prior to live market start
url = 'replay.truedata.in'

symbols = ['NIFTY 50']

td_obj = TD(username, password, live_port=realtime_port, url=url, log_level=logging.DEBUG, log_format="%(message)s")

print('\nStarting Real Time Feed.... ')

req_ids = td_obj.start_live_data(symbols)
live_data_objs = {}

time.sleep(1)

for req_id in req_ids:
    live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])

while True:
    for req_id in req_ids:
        if not td_obj.live_data[req_id] == live_data_objs[req_id]:
            print(f'{td_obj.live_data[req_id].symbol} > {td_obj.live_data[req_id].ltp} > {td_obj.live_data[req_id].change:.2f}')
            live_data_objs[req_id] = deepcopy(td_obj.live_data[req_id])