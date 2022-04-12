from django.urls import path
from .consumers import *

ws_urlpatterns = [
    path('ws/testing/',TestingConsumer.as_asgi()),
    path('ws/bankNifty/',BankNiftyConsumer.as_asgi()),
    path('ws/optionchain/<chain_type>/<exp_date>/',OptionChainConsumer.as_asgi()),
    path('ws/futureOiAnalysis/',FutureOiConsumer.as_asgi()),
]  