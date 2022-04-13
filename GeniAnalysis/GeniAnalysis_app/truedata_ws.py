import websocket
import json
from truedata_ws.websocket.TD import TD
import logging

class TrueDataWS:
    def __init__(self, url, port, username, password, symbols,verbose=True):
        self.url = url
        self.port = port
        self.username = username
        self.password = password
        self.verbose = verbose
        self.data = {"method":"addsymbol","symbols":symbols}
        self.connect()
    
    def verbose_out(self, data):
        if self.verbose:
            print(data)
    
    def connect(self):
        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            f"wss://{self.url}:{self.port}?user={self.username}&password={self.password}",
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(ping_interval=10, ping_timeout=5)
        
    def on_message(self, *args):
        message = args[-1]
        self.verbose_out(message.get('trade', ""))
        return message

    def on_error(self, *args):
        error = args[-1]
        self.verbose_out(error)

    def on_close(self, *args):
        self.ws.close()
        self.verbose_out("### closed ###")

    def on_open(self, *args):
        self.ws.send(json.dumps(self.data))


if __name__ == "__main__":
    symbols = ['NIFTY 50', 'NIFTY BANK', 'NIFTY-I', 'INDIA VIX', 'BANKNIFTY-I']
    # ts = TrueDataWS('push.truedata.in', '8084', 'tdws199', 'ashish@199_stockgini2', symbols)
    # ts.send_symbols()
    # data = ts.on_message()
    # print(data)
    td_app = TD("tdws199", "ashish@199_stockgini2", url="push.truedata.in", live_port="8084", log_level= logging.WARNING)
