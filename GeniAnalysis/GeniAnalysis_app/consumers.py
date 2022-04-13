from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
import requests
import json
import time
import asyncio
from channels.layers import get_channel_layer
from websocket import create_connection
# from . import ws
import datetime
from copy import deepcopy
from . import req_ids, td_app, symbols, nifty_chain, bank_nifty_chain
from datetime import datetime as dt
import traceback
from datetime import timedelta, date
from datetime import time as dt_time



channel_layer = get_channel_layer()


class TestingConsumer(AsyncJsonWebsocketConsumer):
	def __init__(self, *args, **kwargs):
		super(TestingConsumer, self).__init__(*args, **kwargs)
		self.disconnected = True

	async def connect(self):
		await self.channel_layer.group_add('coins', self.channel_name)
		await self.accept()
		self.connected = True
			
		print("Connected to the socket\n")

		# ws = ''
		live_data_objs = {}
		data = {}
		try:
			self.loop = True
			def default(o):
				if isinstance(o, (datetime.date, datetime.datetime)): 
					return o.isoformat()
					
			# for req_id in req_ids:
				# live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])	 
			
			check_time = dt.now().time()
			count = 1
			nifty_ids = [2000, 2002, 2003]
			while self.loop:
				try:
					if date.today().weekday() == 5 or date.today().weekday() == 6:
						await asyncio.sleep(1)
						for req_id in nifty_ids:
							if count <= 3:
								temp_dict = {}
								live_data = td_app.touchline_data[req_id]
								
								temp_dict['symbol'] = live_data.symbol
								temp_dict['day_high'] = live_data.high
								temp_dict['day_low'] = live_data.low
								temp_dict['ltp'] = live_data.ltp
								temp_dict['prev_day_close'] = live_data.prev_close
								temp_dict['day_open'] = live_data.open
								temp_dict['timestamp'] = live_data.timestamp.isoformat()
								temp_dict['_change_perc'] = 0.0
								
								# option_chain = nifty_chain.get_option_chain()
								
								data['live_data'] = json.dumps(temp_dict)
								# data['option_chain'] = json.dumps(option_chain.to_dict('records'), default=default)
								
								await self.send_json(data)
								count = count + 1
					else:
						if (check_time >= dt_time(9,15) and check_time <= dt_time(15,30)):
							await asyncio.sleep(.001)
							for req_id in nifty_ids:
								live_data = vars(td_app.live_data[req_id])
										
								temp_live_data = td_app.live_data[req_id]
								
								live_data['new_change'] = temp_live_data.change_perc
								
								new_live_data = json.dumps(live_data, default=default)
								
								# option_chain = nifty_chain.get_option_chain()
								
								data['live_data'] = new_live_data
								# data['option_chain'] = json.dumps(option_chain.to_dict('records'), default=default)
								
								await self.send_json(data)  

							# for req_id in req_ids:
								# if not td_app.live_data[req_id] == live_data_objs[req_id]:
									# if req_id == 2000 or req_id == 2002 or req_id == 2003:
										# live_data = vars(td_app.live_data[req_id])
										
										# temp_live_data = td_app.live_data[req_id]
										
										# live_data['new_change'] = temp_live_data.change_perc
										
										# new_live_data = json.dumps(live_data, default=default)
										
										
										# option_chain = nifty_chain.get_option_chain()
										
										# data['live_data'] = new_live_data
										# data['option_chain'] = json.dumps(option_chain.to_dict('records'), default=default)
										
										# await self.send(json.dumps(data))	 

										# live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])
								# else:
									# pass 
						else:
							await asyncio.sleep(1)
							
							for req_id in nifty_ids:
								if count <= 3:
									temp_dict = {}
									live_data = td_app.touchline_data[req_id]
									
									temp_dict['symbol'] = live_data.symbol
									temp_dict['day_high'] = live_data.high
									temp_dict['day_low'] = live_data.low
									temp_dict['ltp'] = live_data.ltp
									temp_dict['prev_day_close'] = live_data.prev_close
									temp_dict['day_open'] = live_data.open
									temp_dict['timestamp'] = live_data.timestamp.isoformat()
									temp_dict['_change_perc'] = 0.0
									
									# option_chain = nifty_chain.get_option_chain()
									
									data['live_data'] = json.dumps(temp_dict)
									# data['option_chain'] = json.dumps(option_chain.to_dict('records'), default=default)
									
									await self.send_json(data)
									count = count + 1
				except:
					pass
		except ConnectionError as error:
			exit()

		self.disconnected = False
	   
 
	async def disconnect(self, code):
		await self.channel_layer.group_discard('coins', self.channel_name)
		self.connected = False
		self.disconnected = True
	

class BankNiftyConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.channel_layer.group_add('bank', self.channel_name)
		await self.accept()
		self.connected = True
'''
		live_data_objs = {} 
		data = {}
		try:
			self.loop = True
			def default(o):
				if isinstance(o, (datetime.date, datetime.datetime)):
					return o.isoformat()
					
			for req_id in req_ids:
				live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])
			
			check_time = dt.now().time()
			count = 1
			bank_nifty_ids = [2001, 2003, 2004]
			while self.loop:
				if date.today().weekday() == 5 or date.today().weekday() == 6:
					await asyncio.sleep(1)
					for req_id in bank_nifty_ids:
						if count <= 3:
							temp_dict = {}
							live_data = td_app.touchline_data[req_id]
							
							temp_dict['symbol'] = live_data.symbol
							temp_dict['day_high'] = live_data.high
							temp_dict['day_low'] = live_data.low
							temp_dict['ltp'] = live_data.ltp
							temp_dict['prev_day_close'] = live_data.prev_close
							temp_dict['day_open'] = live_data.open
							temp_dict['timestamp'] = live_data.timestamp.isoformat()
							temp_dict['_change_perc'] = 0.0
							
							option_chain = bank_nifty_chain.get_option_chain()
							
							data['live_data'] = json.dumps(temp_dict)
							data['option_chain'] = json.dumps(option_chain.to_dict('records'), default=default)
							
							await self.send(json.dumps(data))
							count = count + 1
				else:
					if (check_time >= dt_time(9,15) and check_time <= dt_time(15,30)):
						await asyncio.sleep(.001)
						for req_id in req_ids:
							if not td_app.live_data[req_id] == live_data_objs[req_id]:
								if req_id == 2001 or req_id == 2003 or req_id == 2004:
									live_data = vars(td_app.live_data[req_id])
									
									temp_live_data = td_app.live_data[req_id]
									
									live_data['new_change'] = temp_live_data.change_perc
									
									new_live_data = json.dumps(live_data, default=default)
									
									
									option_chain = bank_nifty_chain.get_option_chain()
									
									data['live_data'] = new_live_data
									data['option_chain'] = json.dumps(option_chain.to_dict('records'), default=default)
									
									await self.send(json.dumps(data))

									live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])
							else:
								pass 
					else:
						await asyncio.sleep(1)
						for req_id in bank_nifty_ids:
							if count <= 3:
								temp_dict = {}
								live_data = td_app.touchline_data[req_id]
								
								temp_dict['symbol'] = live_data.symbol
								temp_dict['day_high'] = live_data.high
								temp_dict['day_low'] = live_data.low
								temp_dict['ltp'] = live_data.ltp
								temp_dict['prev_day_close'] = live_data.prev_close
								temp_dict['day_open'] = live_data.open
								temp_dict['timestamp'] = live_data.timestamp.isoformat()
								temp_dict['_change_perc'] = 0.0
								
								option_chain = bank_nifty_chain.get_option_chain()
								
								data['live_data'] = json.dumps(temp_dict)
								data['option_chain'] = json.dumps(option_chain.to_dict('records'), default=default)
								
								await self.send(json.dumps(data))
								count = count + 1

		except ConnectionError as error:
			exit()
	   
 
	async def disconnect(self, code):
		await self.channel_layer.group_discard('bank', self.channel_name)
		self.connected = False

'''
class OptionChainConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.channel_layer.group_add('Test', self.channel_name)
		await self.accept()
	   
		print("Connected to the socket\n")
'''		
		def default(o):
			if isinstance(o, (datetime.date, datetime.datetime)):
				return o.isoformat()

		self.chain_type = self.scope['url_route']['kwargs']['chain_type']
		self.exp_date = self.scope['url_route']['kwargs']['exp_date']

		self.new_exp_date = datetime.datetime.strptime(self.exp_date, '%d %b %Y')

		data = {}
		symbol = str(self.chain_type)
		day = int(self.new_exp_date.day)
		month = int(self.new_exp_date.month)
		year = int(self.new_exp_date.year)
		
		# print(dt(year, month, day))
		
		try:
			self.loop = True
			live_data_objs = {}
			self.option_chain = td_app.start_option_chain(symbol, dt(year, month, day), chain_length = 25, bid_ask = False)
			time.sleep(1)
			 
			for req_id in req_ids:
				live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])
			
			check_time = dt.now().time()
			count = 1
			
			while self.loop:
				if date.today().weekday() == 5 or date.today().weekday() == 6:
					await asyncio.sleep(1)
					# print('hello')
					for req_id in req_ids:
						if count <= 3:
							# print('hello')
							temp_dict = {}
							if req_id == 2000 or req_id == 2001:
								live_data = td_app.touchline_data[req_id]
								
								temp_dict['symbol'] = live_data.symbol
								temp_dict['day_high'] = live_data.high
								temp_dict['day_low'] = live_data.low
								temp_dict['ltp'] = live_data.ltp
								temp_dict['prev_day_close'] = live_data.prev_close
								temp_dict['day_open'] = live_data.open
								temp_dict['timestamp'] = live_data.timestamp
								temp_dict['change_perc'] = 0.0
								
								new_live_data = json.dumps(temp_dict, default=default)
								
								option_chain = self.option_chain.get_option_chain()
								
								data['live_data'] = new_live_data
								data['option_chain'] = json.dumps(option_chain.to_dict('records'), default=default)
								
								await self.send(json.dumps(data))
								count = count + 1
				else:
					if (check_time >= dt_time(9,15) and check_time <= dt_time(15,30)):
						await asyncio.sleep(.001)
						for req_id in req_ids:
							if not td_app.live_data[req_id] == live_data_objs[req_id]:
								if req_id == 2000 or req_id == 2001:
									live_data = td_app.live_data[req_id].to_dict()
									
									temp_live_data = td_app.live_data[req_id]
									
									live_data['new_change'] = temp_live_data.change_perc
									
									new_live_data = json.dumps(live_data, default=default)
									
									option_chain = self.option_chain.get_option_chain()
									
									data['live_data'] = new_live_data
									data['option_chain'] = json.dumps(option_chain.to_dict('records'), default=default)
									
									await self.send(json.dumps(data))

									live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])
							else:
								pass
					else:
						await asyncio.sleep(1)
						# print('hello')
						for req_id in req_ids:
							if count <= 3:
								# print('hello')
								temp_dict = {}
								if req_id == 2000 or req_id == 2001:
									live_data = td_app.touchline_data[req_id]
									
									temp_dict['symbol'] = live_data.symbol
									temp_dict['day_high'] = live_data.high
									temp_dict['day_low'] = live_data.low
									temp_dict['ltp'] = live_data.ltp
									temp_dict['prev_day_close'] = live_data.prev_close
									temp_dict['day_open'] = live_data.open
									temp_dict['timestamp'] = live_data.timestamp
									temp_dict['change_perc'] = 0.0
									
									new_live_data = json.dumps(temp_dict, default=default)
									
									option_chain = self.option_chain.get_option_chain()
									
									data['live_data'] = new_live_data
									data['option_chain'] = json.dumps(option_chain.to_dict('records'), default=default)
									
									await self.send(json.dumps(data))
									count = count + 1
			# elif symbol == "BANKNIFTY":
				# while True:
					# await asyncio.sleep(.001)
					# for req_id in req_ids:
						# if not td_app.live_data[req_id] == live_data_objs[req_id]:
							# if req_id == 2001:
								# live_data = vars(td_app.live_data[req_id])
								
								# new_live_data = json.dumps(live_data, default=default)
								
								# option_chain = self.option_chain.get_option_chain()
								
								# data['live_data'] = new_live_data
								# data['option_chain'] = json.dumps(option_chain.to_dict('records'), default=default)
								
								# await self.send(json.dumps(data))

								# live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])
						# else:
							# pass

			# while True:
				# await asyncio.sleep(1)
				# my_option_chain = self.option_chain.get_option_chain()
						  
				# data['live_data'] = ''
				# data['option_chain'] = json.dumps(my_option_chain.to_dict('records'), default=default)
				
				# await self.send(json.dumps(data))
				
			
		except:
			traceback.print_exc()
			data['option_chain'] = 'Error'
			await self.send(json.dumps(data))

	async def disconnect(self, code):
		try:
			self.option_chain.stop_option_chain()
		except:
			pass
			
		await self.channel_layer.group_discard('Test', self.channel_name)
		
'''		
class FutureOiConsumer(AsyncWebsocketConsumer): 
	async def connect(self):
		await self.channel_layer.group_add('coins', self.channel_name)
		await self.accept()
		self.connected = True
			
		print("Connected to the socket\n")

'''
		# ws = ''
		live_data_objs = {}
		data = {}
		try:
			self.loop = True
			def default(o):
				if isinstance(o, (datetime.date, datetime.datetime)): 
					return o.isoformat()
					
			for req_id in req_ids:
				live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])	 
			
			check_time = dt.now().time()
			count = 1
			while self.loop:
				if date.today().weekday() == 5 or date.today().weekday() == 6:
					await asyncio.sleep(1)
					for req_id in req_ids:
						if count <= 3:
							temp_dict = {}
							if req_id != 2000 and req_id != 2001 and req_id != 2003:
								live_data = td_app.touchline_data[req_id]
								
								temp_dict['symbol'] = live_data.symbol
								temp_dict['day_high'] = live_data.high
								temp_dict['day_low'] = live_data.low
								temp_dict['ltp'] = live_data.ltp
								temp_dict['prev_day_close'] = live_data.prev_close
								temp_dict['day_open'] = live_data.open
								temp_dict['timestamp'] = live_data.timestamp
								temp_dict['_change_perc'] = 0.0
								
								new_live_data = json.dumps(temp_dict, default=default)
								
								option_chain = nifty_chain.get_option_chain()
								
								data['live_data'] = new_live_data
								data['option_chain'] = json.dumps(option_chain.to_dict('records'), default=default)
								
								await self.send(json.dumps(data))
								count = count + 1
				else:
					if (check_time >= dt_time(9,15) and check_time <= dt_time(15,30)):
						await asyncio.sleep(.001)
						for req_id in req_ids:
							# print(req_id)
							if not td_app.live_data[req_id] == live_data_objs[req_id]:
								# if req_id == 2000 or req_id == 2002 or req_id == 2003:
								if req_id != 2000 and req_id != 2001 and req_id != 2003:
									live_data = td_app.live_data[req_id].to_dict()
									
									new_live_data = json.dumps(live_data, default=default)
									
									data['live_data'] = new_live_data
									
									await self.send(json.dumps(data))  

									live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])
							else:
								pass  
					else: 
						await asyncio.sleep(1)
						for req_id in req_ids:
							if count <= 3:
								temp_dict = {}
								if req_id != 2000 and req_id != 2001 and req_id != 2003:
									# print(td_app.touchline_data[req_id])
									live_data = td_app.touchline_data[req_id]
									# print(live_data)
									# temp_dict['symbol'] = live_data.symbol
									# temp_dict['ltp'] = live_data.ltp
									# temp_dict['change'] = live_data.change
									# temp_dict['change_perc'] = live_data.change_perc
									# temp_dict['oi'] = live_data.oi
									# temp_dict['oi_change'] = live_data.oi_change
									# temp_dict['oi_change_perc'] = live_data.oi_change_perc
									# temp_dict['ttq'] = live_data.ttq
									temp_dict['symbol'] = live_data.symbol
									temp_dict['ltp'] = live_data.ltp
									temp_dict['change'] = 0.0
									temp_dict['change_perc'] = 0.0
									temp_dict['oi'] = live_data.oi
									temp_dict['oi_change'] = 0.0
									temp_dict['oi_change_perc'] = 0.0
									temp_dict['ttq'] = live_data.ttq
									
									new_live_data = json.dumps(temp_dict, default=default)
									
									data['live_data'] = new_live_data
									
									await self.send(json.dumps(data))
									count = count + 1
					
						 
		except ConnectionError as error:
			print('Testing Consumer ----------------------- ', error)
			exit()
	   
 
	async def disconnect(self, code):
		await self.channel_layer.group_discard('coins', self.channel_name)
		self.connected = False
'''