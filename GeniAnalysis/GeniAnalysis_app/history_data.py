from truedata_ws.websocket.TD import TD
from copy import deepcopy
import time
import logging
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd

pd.set_option("display.max_columns", None, "display.max_rows", None)

truedata_development_username = 'tdws199'
truedata_development_password = 'ashish@199_stockgini_x'
truedata_development_port = '8084'

td_obj = TD(truedata_development_username, truedata_development_password, live_port=8084, log_level= logging.WARNING)  # for option chain

# hist_data_1 = td_app.get_historic_data('BANKNIFTY-I')
# hist_data_2 = td_obj.get_historic_data('BANKNIFTY-I', duration='1 D')
# hist_data_3 = td_obj.get_historic_data('BANKNIFTY-I', bar_size='30 mins')
# hist_data_4 = td_obj.get_historic_data('BANKNIFTY-I', start_time=dt.now()-relativedelta(days=3))

hist_data_5 = td_obj.get_historic_data('BANKNIFTY-I', end_time=datetime(2022, 4, 5, 15, 30))

# hist_data_7 = td_obj.get_historic_data('BANKNIFTY-I', duration='1 D', bar_size='tick', bidask=False)

print(hist_data_5)
# df = pd.DataFrame(hist_data_5)

# print(df)