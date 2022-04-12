default_app_config = "GeniAnalysis_app.apps.GenianalysisAppConfig"


# using Truedata library


from truedata_ws.websocket.TD import TD
from copy import deepcopy

import logging

import pandas as pd
import requests
from datetime import date, timedelta

import time

from . import credentials

from truedata_ws.websocket.TD import TD
from copy import deepcopy
import time
import logging
from datetime import datetime as dt
import pandas as pd
pd.set_option("display.max_columns", None, "display.max_rows", None)

# username = credentials.truedata_development_username
# password = credentials.truedata_development_password
# realtime_port = credentials.truedata_development_port

username = credentials.truedata_production_username
password = credentials.truedata_production_password
realtime_port = credentials.truedata_production_port
# url = 'replay.truedata.in'
url = 'push.truedata.in' 

try:
	# td_app = TD(username, password, live_port=8084, url=url,	log_level= logging.WARNING)	 # for option chain
	td_app = TD(username, password, url=url, live_port=realtime_port, log_level= logging.WARNING)  # for option chain
	
except:
	td_app.stop_live_data(symbols)
	td_app.disconnect()

symbols = ['NIFTY 50', 'NIFTY BANK', 'NIFTY-I', 'INDIA VIX', 'BANKNIFTY-I']

symbols1 = [
	'NIFTY 50', 'NIFTY BANK', 'NIFTY-I', 'INDIA VIX', 'BANKNIFTY-I','FINNIFTY-I',
	'AARTIIND-I','ABB-I','ABBOTINDIA-I','ABCAPITAL-I','ABFRL-I','ACC-I',
	'ADANIENT-I','ADANIPORTS-I','ALKEM-I','AMARAJABAT-I','AMBUJACEM-I',
	'APLLTD-I','APOLLOHOSP-I','APOLLOTYRE-I','ASHOKLEY-I','ASIANPAINT-I',
	'ASTRAL-I','ATUL-I','AUBANK-I','AUROPHARMA-I','AXISBANK-I','BAJAJ-AUTO-I',
	'BAJAJFINSV-I','BAJFINANCE-I','BALKRISIND-I','BALRAMCHIN-I','BANDHANBNK-I',
	'BANKBARODA-I','BATAINDIA-I','BEL-I','BERGEPAINT-I','BHARATFORG-I','BHARTIARTL-I',
	'BHEL-I','BIOCON-I','BOSCHLTD-I','BPCL-I','BRITANNIA-I','BSOFT-I','CANBK-I',
	'CANFINHOME-I','CHAMBLFERT-I','CHOLAFIN-I','CIPLA-I','COALINDIA-I','COFORGE-I',
	'COLPAL-I','CONCOR-I','COROMANDEL-I','CROMPTON-I','CUB-I','CUMMINSIND-I','DABUR-I',
	'DALBHARAT-I','DEEPAKNTR-I','DELTACORP-I','DIVISLAB-I','DIXON-I','DLF-I','DRREDDY-I',
	'EICHERMOT-I','ESCORTS-I','EXIDEIND-I','FEDERALBNK-I','FSL-I','GAIL-I','GLENMARK-I',
	'GMRINFRA-I','GNFC-I','GODREJCP-I','GODREJPROP-I','GRANULES-I','GRASIM-I','GSPL-I',
	'GUJGASLTD-I','HAL-I','HAVELLS-I','HCLTECH-I','HDFC-I','HDFCAMC-I','HDFCBANK-I',
	'HDFCLIFE-I','HEROMOTOCO-I','HINDALCO-I','HINDCOPPER-I','HINDPETRO-I','HINDUNILVR-I',
	'HONAUT-I','IBULHSGFIN-I','ICICIBANK-I','ICICIGI-I','ICICIPRULI-I','IDEA-I','IDFC-I',
	'IDFCFIRSTB-I','IEX-I','IGL-I','INDHOTEL-I','INDIACEM-I','INDIAMART-I','INDIGO-I',
	'INDUSINDBK-I','INDUSTOWER-I','INFY-I','INTELLECT-I','IOC-I','IPCALAB-I','IRCTC-I',
	'ITC-I','JINDALSTEL-I','JKCEMENT-I','JSWSTEEL-I','JUBLFOOD-I','KOTAKBANK-I','L&TFH-I',
	'LALPATHLAB-I','LAURUSLABS-I','LICHSGFIN-I','LT-I','LTI-I','LTTS-I','LUPIN-I','M&M-I',
	'M&MFIN-I','MANAPPURAM-I','MARICO-I','MARUTI-I','MCDOWELL-N-I','MCX-I','METROPOLIS-I',
	'MFSL-I','MGL-I','MINDTREE-I','MOTHERSUMI-I','MPHASIS-I','MRF-I','MUTHOOTFIN-I',
	'NAM-INDIA-I','NATIONALUM-I','NAUKRI-I','NAVINFLUOR-I','NBCC-I','NESTLEIND-I','NMDC-I',
	'NTPC-I','OBEROIRLTY-I','OFSS-I','ONGC-I','PAGEIND-I','PEL-I','PERSISTENT-I','PETRONET-I',
	'PFC-I','PFIZER-I','PIDILITIND-I','PIIND-I','PNB-I','POLYCAB-I','POWERGRID-I','PVR-I',
	'RAIN-I','RAMCOCEM-I','RBLBANK-I','RECLTD-I','RELIANCE-I','SAIL-I','SBICARD-I','SBILIFE-I',
	'SBIN-I','SHREECEM-I','SIEMENS-I','SRF-I','SRTRANSFIN-I','STAR-I','SUNPHARMA-I','SUNTV-I',
	'SYNGENE-I','TATACHEM-I','TATACOMM-I','TATACONSUM-I','TATAMOTORS-I','TATAPOWER-I','TATASTEEL-I',
	'TCS-I','TECHM-I','TITAN-I','TORNTPHARM-I','TORNTPOWER-I','TRENT-I','TVSMOTOR-I','UBL-I','ULTRACEMCO-I',
	'UPL-I','VEDL-I','VOLTAS-I','WHIRLPOOL-I','WIPRO-I','ZEEL-I','ZYDUSLIFE-I',
	]


print('Starting Real Time Feed.... ')

print(f'Port > {realtime_port}')  



req_ids = td_app.start_live_data(symbols1)

print()
 
time.sleep(1) 

d = dt.now().date()
weekday = 3
days_ahead = weekday - d.weekday()
if days_ahead < 0:
	days_ahead += 7
next_thursday = d + timedelta(days_ahead)

day = int(next_thursday.day)
month = int(next_thursday.month)
year = int(next_thursday.year)

# pload = {'date':next_thursday}
# r = requests.post('http://172.105.57.86:8050/check_thursday/',data = pload)
# print(r.json())

# nifty_chain = td_app.start_option_chain('NIFTY', dt(year, month, day), chain_length = 25, bid_ask = False)
# bank_nifty_chain = td_app.start_option_chain('BANKNIFTY', dt(year, month, day), chain_length = 25, bid_ask = False)
nifty_chain = td_app.start_option_chain('NIFTY', dt(year, month, 13), chain_length = 25, bid_ask = False)
bank_nifty_chain = td_app.start_option_chain('BANKNIFTY', dt(year, month, 13), chain_length = 25, bid_ask = False)

time.sleep(2)
