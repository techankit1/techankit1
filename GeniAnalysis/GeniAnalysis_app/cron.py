from .models import TestingTime

def my_cron_job():
    testingTime = TestingTime()
    testingTime.save()
		
		


# try:
	# f = open('HistoryData.txt','a+')
	# f.write("History option data")
	# import os
	# import traceback
	# import django
	# import sys
	# script_path = sys.path.append('/home/ubuntu/StockGeni')
	# os.environ['DJANGO_SETTINGS_MODULE']='StockGeni.settings'
	# django.setup()
	# from StockGeni_app.models import *
	# from django.shortcuts import render, redirect
	# from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
	# from django.views.decorators.csrf import csrf_exempt
	# from django.conf import settings
	# from StockGeni_app.views import my_cron_job
	# from datetime import date, datetime, time
	
	# print("datetime..............", datetime.now())
		
	# count = 0
		
	# while True:
		# if count == 0:
			# my_cron_job()
			# count += 1
		# else:
			# break
			
# except Exception as e:
	# f.write('\n' + str(e))
	# print(str(e))
	# print(traceback.format_exc())
	# td_app.stop_live_data(symbols)
	# td_app.disconnect()