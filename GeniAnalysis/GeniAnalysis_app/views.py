import itertools
from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import EmailMessage
from .models import *
from datetime import datetime, timedelta, time, date
from django.template.loader import get_template, render_to_string
import string, json
import base64
import random
import operator
import math
import os
import traceback
from django.db.models import Q	 
import requests
from truedata_ws.websocket.TD import TD
import pandas as pd
import datetime as dt
from timeloop import Timeloop
from copy import deepcopy
import string
import random
from django.views.decorators.cache import cache_control
import calendar
import schedule
import time as t
from django.utils import timezone
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from . import credentials
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage

def send_email(subject, string, to_email):
	try:
		from_email = settings.EMAIL_HOST_USER
		email_msg = EmailMultiAlternatives(subject, string ,from_email = from_email, to=[to_email])
		email_msg.mixed_subtype = 'related'
		email_msg.attach_alternative(string, "text/html")
		email_msg.send()
		return "success"
	except Exception as e:
		print(str(traceback.format_exc()))
		return "error"
# import sweetify
 

from . import req_ids, td_app, symbols, nifty_chain, bank_nifty_chain



tl = Timeloop()

@tl.job(interval=timedelta(seconds=60))
def my_cron_job():
	if date.today().weekday() == 5 or date.today().weekday() == 6:
		pass
	else:
		check_time = datetime.now().time()	
		
		if (check_time >= time(9,15) and check_time <= time(15,31)):
			live_data_objs = {}
			
			for req_id in req_ids:
				if req_id == 2000: 
					live_data = td_app.live_data[req_id].__dict__
			
			if (check_time >= time(9,20) and check_time < time(9,21)):
				SaveOpenModel.objects.create(open_val=live_data['day_open'])
				
			if (check_time >= time(9,30) and check_time < time(9,31)):
				GannHighLow.objects.create(high_val=live_data['day_high'], low_val = live_data['day_low'])
			
			option_chain = nifty_chain.get_option_chain()
			
			row_data = option_chain.to_dict('records')
			obj = ""
			
			total_call_change_oi_val = 0
			total_put_change_oi_val = 0
			
			for row in row_data:
				if row['type'] == 'CE':
					obj = HistoryLog.objects.create(strike_price=row['strike'], call_change_oi=row['oi_change'], ltp=live_data['ltp'], call_oi=row['oi'], call_ltp=row['ltp'])
					total_call_change_oi_val = total_call_change_oi_val + int(row['oi_change'])
				else:
					HistoryLog.objects.filter(id=obj.id).update(put_change_oi=row['oi_change'], put_oi=row['oi'], put_ltp=row['ltp'])
					total_put_change_oi_val = total_put_change_oi_val + int(row['oi_change'])
			SumOfOiLog.objects.create(total_call_change_oi=total_call_change_oi_val, total_put_change_oi=total_put_change_oi_val)
		else: 
			pass
tl.start()

t2 = Timeloop()

@t2.job(interval=timedelta(seconds=60))
def my_cron_job1():
	if date.today().weekday() == 5 or date.today().weekday() == 6:
		pass
	else: 
		check_time = datetime.now().time()
		
		if (check_time >= time(9,15) and check_time <= time(15,31)):
			live_data_objs = {}
			
			for req_id in req_ids:
				if req_id == 2001:
					live_data = td_app.live_data[req_id].__dict__
			
			if (check_time >= time(9,20) and check_time < time(9,21)):
				BnfSaveOpenModel.objects.create(open_val=live_data['day_open'])
				
			if (check_time >= time(9,30) and check_time < time(9,31)):
				BnfGannHighLow.objects.create(high_val=live_data['day_high'], low_val=live_data['day_low'])
			
			option_chain = bank_nifty_chain.get_option_chain()
			
			row_data = option_chain.to_dict('records')
			obj = ""
			
			total_call_change_oi_val = 0
			total_put_change_oi_val = 0
			
			for row in row_data:
				if row['type'] == 'CE':
					obj = BnfHistoryLog.objects.create(strike_price=row['strike'], call_change_oi=row['oi_change'], ltp=live_data['ltp'], call_oi=row['oi'], call_ltp=row['ltp'])
					total_call_change_oi_val = total_call_change_oi_val + int(row['oi_change'])
				else:
					BnfHistoryLog.objects.filter(id=obj.id).update(put_change_oi=row['oi_change'], put_oi=row['oi'], put_ltp=row['ltp'])
					total_put_change_oi_val = total_put_change_oi_val + int(row['oi_change'])
			BnfSumOfOiLog.objects.create(total_call_change_oi=total_call_change_oi_val, total_put_change_oi=total_put_change_oi_val)
		else: 
			pass	
	
t2.start()
	
t3 = Timeloop()

@t3.job(interval=timedelta(seconds=60))
def my_cron_job2():
	if date.today().weekday() == 5 or date.today().weekday() == 6:
		pass
	else: 
		check_time = datetime.now().time()
		
		if (check_time >= time(9,15) and check_time <= time(15,31)):
			live_data_objs = {}
			
			for req_id in req_ids:
				if req_id != 2000 and req_id != 2001 and req_id != 2003:
					live_data = td_app.live_data[req_id].to_dict()
					IntradayFutureAnalysis.objects.create(symbol=live_data['symbol'], last_price=live_data['ltp'], price_change=live_data['change'], oi_change=live_data['oi_change'], oi = live_data['oi'])
			
		else:		   
			pass	
	
t3.start()	


######## MASTER FUNCTIONS ##############
def next_weekday(d, weekday):
	days_ahead = weekday - d.weekday()
	if days_ahead <= 0: # Target day already happened this week
		days_ahead += 7
	return d + timedelta(days_ahead)
######## MASTER FUNCTIONS ##############
 
######################### RENDERED PAGES ######################################

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def gannAnglesDashboard(request):
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---'
			user_obj.current_active_status = 'Inactive'
		if user_obj.login_token == login_token:
			return render(request, 'Panel/dashboard-gann-angles.html', {'user':user_obj})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')
		
@csrf_exempt
def get_gann_values(request):
	if request.method == 'POST':
		gann_type = request.POST.get('type')
		
		if gann_type == 'NIFTY':
			try:			
				# histroy_obj = SumOfOiLog.objects.filter(today_date=date.today()).values()
				gann_values = GannHighLow.objects.filter(today_date=date.today()).values()
				
				return JsonResponse({"status":"1",'data': list(gann_values)})
			except:
				traceback.print_exc()
				return JsonResponse({"status":"0",'msg': 'Something went wrong'})
		elif gann_type == 'BANKNIFTY':
			try:			
				# histroy_obj = SumOfOiLog.objects.filter(today_date=date.today()).values()
				gann_values = BnfGannHighLow.objects.filter(today_date=date.today()).values()
				
				return JsonResponse({"status":"1",'data': list(gann_values)})
			except:
				traceback.print_exc()
				return JsonResponse({"status":"0",'msg': 'Something went wrong'})

	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})

def termsAndCondition(request):
	return render(request, 'Website/terms-condition.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def websiteHomePage(request):
	monthly_subscription = Subscription_Plan.objects.filter(subscription_type="Monthly", status="Active").last()
	yearly_subscription = Subscription_Plan.objects.filter(subscription_type="Yearly", status="Active").last()
	
	# print(monthly_subscription.subscription_type)
	return render(request, 'Website/index-1.html',{'monthly_subscription':monthly_subscription,'yearly_subscription':yearly_subscription})
	
@csrf_exempt
def user_login_page(request):
	return render(request, 'Panel/login.html')
	
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True)
def logout_api(request):
	try:
		if request.session.get("user_id") or request.session.get('login_token'):
			UserDetails.objects.filter(id=request.session['user_id']).update(is_login=False)
			del request.session['user_id']
			del request.session['login_token']
		return redirect('/login/')
	except:
		return redirect('/login/')
	
@csrf_exempt
def user_signup_page(request):
	return render(request, 'Panel/signup.html')
	
	
@csrf_exempt
def user_dashboard_page(request):
	return render(request, 'Panel/index.html')
	

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_nifty_dashboard_page(request):
	############ common code to write on each reder view funtion ############
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---'
			user_obj.current_active_status = 'Inactive'
	############ common code to write on each reder view funtion ############
	
		if user_obj.login_token == login_token:
			d = dt.now().date()
			date_list = []
			weekday = 3
			
			if (d.weekday() == 3):
				temp_date = f"{int(d.day)} {calendar.month_abbr[int(d.month)]} {int(d.year)}"
				date_list.append(temp_date)
			
			for i in range(6):
				days_ahead = weekday - d.weekday()
				if days_ahead <= 0:
					days_ahead += 7
				next_thursday = d + timedelta(days_ahead)
				
				d = next_thursday
				
				temp_date = f"{int(next_thursday.day)} {calendar.month_abbr[int(next_thursday.month)]} {int(next_thursday.year)}"
				date_list.append(temp_date)
			
			if HistoryLogInterval.objects.filter(user=user_obj).exists() and NiftySentiments.objects.filter(user=user_obj).exists():
				interval_obj = HistoryLogInterval.objects.get(user=user_obj)
				sentiments_obj = NiftySentiments.objects.get(user=user_obj)
				
				return render(request, 'Panel/dashboards-commerce.html', {'interval_obj':interval_obj, 'user':user_obj,'page':'nifty', 'sentiments_obj':sentiments_obj, 'date_list': date_list})
			else:
				interval_obj = ""
				sentiments_obj = ""
				return render(request, 'Panel/dashboards-commerce.html', {'interval_obj':interval_obj, 'user':user_obj,'page':'nifty', 'sentiments_obj':sentiments_obj, 'date_list': date_list})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')
		
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def oi_analysis_dashboard(request):
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---'
			user_obj.current_active_status = 'Inactive'
			
		if user_obj.login_token == login_token:
			d = dt.now().date()
			date_list = []
			weekday = 3
			
			if (d.weekday() == 3):
				temp_date = f"{int(d.day)} {calendar.month_abbr[int(d.month)]} {int(d.year)}"
				date_list.append(temp_date)
			
			for i in range(5):
				days_ahead = weekday - d.weekday()
				if days_ahead <= 0:
					days_ahead += 7
				next_thursday = d + timedelta(days_ahead)
				
				d = next_thursday
				
				temp_date = f"{int(next_thursday.day)} {calendar.month_abbr[int(next_thursday.month)]} {int(next_thursday.year)}"
				date_list.append(temp_date)
				
			return render(request, 'Panel/dashboards-oi-analysis.html', {'user':user_obj, 'date_list':date_list})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')
		
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def future_oi_analysis_dashboard(request):
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---'
			user_obj.current_active_status = 'Inactive'
			
		if user_obj.login_token == login_token:
			return render(request, 'Panel/dashboard_future_oi_analysis.html', {'user':user_obj})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')
		
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def future_graph_analysis_dashboard(request):
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---'
			user_obj.current_active_status = 'Inactive'
			
		if user_obj.login_token == login_token:
			return render(request, 'Panel/dashboard_future_graph_analysis.html', {'user':user_obj})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')
		
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard_intraday_future_oi_analysis(request):
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---'
			user_obj.current_active_status = 'Inactive'
			
		if user_obj.login_token == login_token:
			interval_obj = IntradayFutureAnalysisInterval.objects.filter(user=user_obj).last()
			return render(request, 'Panel/dashboard_intraday_future_oi_analysis.html', {'user':user_obj, 'interval_obj':interval_obj})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')
		
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard_price_vs_oi(request):
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---'
			user_obj.current_active_status = 'Inactive'
			
		if user_obj.login_token == login_token:
			# interval_obj = IntradayFutureAnalysisInterval.objects.filter(user=user_obj).last()
			return render(request, 'Panel/dashboard_price_vs_oi.html', {'user':user_obj})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard_option_price_vs_oi(request):
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---'
			user_obj.current_active_status = 'Inactive'
			
		if user_obj.login_token == login_token:
			Nifty_strike_price = HistoryLog.objects.filter(today_date=date.today()).order_by('-id')[:24]
			BankNifty_strike_price = BnfHistoryLog.objects.filter(today_date=date.today()).order_by('-id')[:24]
			# print(BankNifty_strike_price)
			# interval_obj = IntradayFutureAnalysisInterval.objects.filter(user=user_obj).last()
			return render(request, 'Panel/dashboard_option_price_vs_oi.html', {'user':user_obj,'Nifty_strike_price':Nifty_strike_price,'BankNifty_strike_price':BankNifty_strike_price})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard_oi_chart(request):
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today() - timedelta(days=1), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---' 
			user_obj.current_active_status = 'Inactive'
			
		if user_obj.login_token == login_token:
			check_date = None;
			if date.today().weekday() == 5:
				check_date = date.today() - timedelta(days=1)
			elif date.today().weekday() == 6:
				check_date = date.today() - timedelta(days=2)
			else:
				check_date = date.today()
			
			Nifty_strike_price = HistoryLog.objects.filter(today_date=check_date).order_by('-id')[:24]
			Nifty_strike_price = sorted(Nifty_strike_price, key=operator.attrgetter('strike_price'))
			BankNifty_strike_price = BnfHistoryLog.objects.filter(today_date=check_date).order_by('-id')[:24]
			BankNifty_strike_price = sorted(BankNifty_strike_price, key=operator.attrgetter('strike_price'))
			# interval_obj = IntradayFutureAnalysisInterval.objects.filter(user=user_obj).last()
			
			return render(request, 'Panel/dashboard_oi_chart.html', {'user':user_obj,'Nifty_strike_price':Nifty_strike_price,'BankNifty_strike_price':BankNifty_strike_price})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')
		
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard_three_strike_oi_analysis(request):
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today() - timedelta(days=1), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---' 
			user_obj.current_active_status = 'Inactive'
			
		if user_obj.login_token == login_token:
			check_date = None;
			if date.today().weekday() == 5:
				check_date = date.today() - timedelta(days=1)
			elif date.today().weekday() == 6:
				check_date = date.today() - timedelta(days=2)
			else:
				check_date = date.today()
			
			Nifty_strike_price = HistoryLog.objects.filter(today_date=check_date).order_by('-id')[:24]
			Nifty_strike_price = sorted(Nifty_strike_price, key=operator.attrgetter('strike_price'))
			BankNifty_strike_price = BnfHistoryLog.objects.filter(today_date=check_date).order_by('-id')[:24]
			BankNifty_strike_price = sorted(BankNifty_strike_price, key=operator.attrgetter('strike_price'))
			# interval_obj = IntradayFutureAnalysisInterval.objects.filter(user=user_obj).last()
			
			return render(request, 'Panel/dashboard_three_strike_oi_analysis.html', {'user':user_obj,'Nifty_strike_price':Nifty_strike_price,'BankNifty_strike_price':BankNifty_strike_price})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard_ten_strike_oi_analysis(request):
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today() - timedelta(days=1), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---' 
			user_obj.current_active_status = 'Inactive'
			
		if user_obj.login_token == login_token:
			check_date = None;
			if date.today().weekday() == 5:
				check_date = date.today() - timedelta(days=1)
			elif date.today().weekday() == 6:
				check_date = date.today() - timedelta(days=2)
			else:
				check_date = date.today()
			try:
				Nifty_strike_price = HistoryLog.objects.filter(today_date=check_date).order_by('-id')[:24]
				queryset = Nifty_strike_price[7:17]
				nifty_start = queryset[len(queryset) - 1].strike_price
				nifty_end = queryset[0].strike_price
				# Nifty_strike_price = sorted(Nifty_strike_price, key=operator.attrgetter('strike_price'))
				BankNifty_strike_price = BnfHistoryLog.objects.filter(today_date=check_date).order_by('-id')[:24]
				queryset1 = BankNifty_strike_price[7:17]
				Banknifty_start = queryset1[len(queryset) - 1].strike_price
				Banknifty_end = queryset1[0].strike_price
			except:
				nifty_start = 0
				nifty_end = 0
				Banknifty_start = 0
				Banknifty_end = 0
			# BankNifty_strike_price = sorted(BankNifty_strike_price, key=operator.attrgetter('strike_price'))
			# interval_obj = IntradayFutureAnalysisInterval.objects.filter(user=user_obj).last()
			
			return render(request, 'Panel/dashboard_ten_strike_oi_analysis.html', {'user':user_obj,'nifty_start':nifty_start,'nifty_end':nifty_end,'Banknifty_start':Banknifty_start,'Banknifty_end':Banknifty_end})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')

@csrf_exempt
def get_active_genimode(request):
	if request.method == 'POST':
		geni_type = request.POST.get('geni_type')
		strike_price = request.POST.get('strike_price')
		cur_ltp = request.POST.get('cur_ltp')
		symbol = request.POST.get('symbol')
		selected_strike_price = request.POST.get('selected_strike_price')
		status = request.POST.get('status')
		
		# print(geni_type, strike_price, cur_ltp, symbol, selected_strike_price) 
		
		try:
			if status == 'On':
				if symbol == 'Nifty':
					if GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).exists():
						geni_obj = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).last()
						
						if geni_obj.genimode_type == geni_type:
							geni_obj_list = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).values()
							return JsonResponse({"status":"1",'msg': list(geni_obj_list)})
						else:
							geni_update_obj = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).update(genimode_type=geni_type, genimode_strike_price=strike_price, genimode_current_ltp=cur_ltp, genimode_target=float(cur_ltp)+40,genimode_stop_loss=float(cur_ltp)-30)
							geni_update_obj_list = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).values()
							return JsonResponse({"status":"1",'msg': list(geni_update_obj_list)})
					else:
						geni_created_obj = GeniModeDetails.objects.create(genimode_type=geni_type, genimode_strike_price=strike_price, genimode_current_ltp=cur_ltp, genimode_target=float(cur_ltp)+40,genimode_stop_loss=float(cur_ltp)-30, symbol='Nifty', selected_strike_price=selected_strike_price)
						geni_created_list = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).values()
						return JsonResponse({"status":"1",'msg': list(geni_created_list)})
				elif symbol == 'BankNifty':
					if GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).exists():
						geni_obj = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).last()
						
						if geni_obj.genimode_type == geni_type:
							geni_obj_list = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).values()
							return JsonResponse({"status":"1",'msg': list(geni_obj_list)})
						else:
							geni_update_obj = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).update(genimode_type=geni_type, genimode_strike_price=strike_price, genimode_current_ltp=cur_ltp, genimode_target=float(cur_ltp)+40,genimode_stop_loss=float(cur_ltp)-30)
							geni_update_obj_list = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).values()
							return JsonResponse({"status":"1",'msg': list(geni_update_obj_list)})
					else: 
						geni_created_obj = GeniModeDetails.objects.create(genimode_type=geni_type, genimode_strike_price=strike_price, genimode_current_ltp=cur_ltp, genimode_target=float(cur_ltp)+40,genimode_stop_loss=float(cur_ltp)-30, symbol='BankNifty', selected_strike_price=selected_strike_price)
						geni_created_list = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).values()
						return JsonResponse({"status":"1",'msg': list(geni_created_list)})
				else:
					return JsonResponse({"status":"0",'msg': 'Done'})
					
						
			elif status == 'Off':
				if symbol == 'Nifty': 
					if GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).exists():
						geni_obj = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).update(genimode_type='WAIT', genimode_target_on=False, genimode_stop_loss_on=False)
						return JsonResponse({"status":"1",'msg': 'Done'})
				elif symbol == 'BankNifty': 
					if GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).exists():
						geni_obj = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).update(genimode_type='WAIT', genimode_target_on=False, genimode_stop_loss_on=False)
						return JsonResponse({"status":"1",'msg': 'Done'})
				else:
					return JsonResponse({"status":"1",'msg': 'Done'}) 
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def set_target_stop_loss(request):
	if request.method == 'POST':
		edit_type = request.POST.get('edit_type')
		symbol = request.POST.get('symbol')
		selected_strike_price = request.POST.get('selected_strike_price')
		status = request.POST.get('status')
		
		try:
			if status == 'On':
				if symbol == 'Nifty':
					if GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).exists():
						geni_obj = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).last()
						
						if edit_type == 'target':
							GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).update(genimode_target_on=True)
							return JsonResponse({"status":"1",'msg': 'Done'})
						elif edit_type == 'stop loss':
							GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).update(genimode_stop_loss_on=True)
							return JsonResponse({"status":"1",'msg': 'Done'})
					else:
						return JsonResponse({"status":"0",'msg': 'Not Done'})
				elif symbol == 'BankNifty':
					if GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).exists():
						geni_obj = GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).last()
						
						if edit_type == 'target':
							GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).update(genimode_target_on=True)
							return JsonResponse({"status":"1",'msg': 'Done'})
						elif edit_type == 'stop loss':
							GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).update(genimode_stop_loss_on=True)
							return JsonResponse({"status":"1",'msg': 'Done'})
					else:
						return JsonResponse({"status":"0",'msg': 'Not Done'})
				else:
					return JsonResponse({"status":"1",'msg': 'Done'})
						
			elif status == 'Off':
				if symbol == 'Nifty': 
					if GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).exists():
						GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).update(genimode_target_on=False, genimode_stop_loss_on=False)
						return JsonResponse({"status":"1",'msg': 'Done'})
				elif symbol == 'BankNifty': 
					if GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).exists():
						GeniModeDetails.objects.filter(selected_strike_price=selected_strike_price, today_date=date.today()).update(genimode_target_on=False, genimode_stop_loss_on=False)
						return JsonResponse({"status":"1",'msg': 'Done'})
				else:
					return JsonResponse({"status":"1",'msg': 'Done'}) 
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
	
######################### Ajax to set Interval ######################################

@csrf_exempt
def set_user_interval(request):
	if request.method == 'POST':
		interval_val = request.POST.get('interval_val')
		user_id = request.POST.get('user_id')
		
		try:
			user_obj = UserDetails.objects.get(id=user_id)
			HistoryLogInterval.objects.filter(user=user_obj).update(interval=interval_val)
			
			return JsonResponse({"status":"0",'msg': 'Done'})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def set_intraday_interval(request):
	if request.method == 'POST':
		interval_val = request.POST.get('interval_val')
		user_id = request.POST.get('user_id')
		
		try:
			user_obj = UserDetails.objects.get(id=user_id)
			if IntradayFutureAnalysisInterval.objects.filter(user=user_obj).exists():
				IntradayFutureAnalysisInterval.objects.filter(user=user_obj).update(interval=interval_val)
			else:  
				IntradayFutureAnalysisInterval.objects.create(user=user_obj, interval=interval_val)
			return JsonResponse({"status":"0",'msg': 'Done'})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})

@csrf_exempt
def get_open_val(request):
	if request.method == 'POST':
		try:
			open_value = SaveOpenModel.objects.filter(today_date=date.today()).last().open_val
			
			return JsonResponse({"status":"1",'data': open_value})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def set_user_total_interval(request):
	if request.method == 'POST':
		interval_val = request.POST.get('interval_val')
		user_id = request.POST.get('user_id')
		
		try:
			user_obj = UserDetails.objects.get(id=user_id)
			HistoryLogInterval.objects.filter(user=user_obj).update(interval_total_oi=interval_val)
			
			return JsonResponse({"status":"0",'msg': 'Done'})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})

@csrf_exempt
def history_logging_data(request):
	if request.method == 'POST':
		try:
			strike_price_1_val = request.POST.get('strike_price1')
			strike_price_2_val = request.POST.get('strike_price2')
			strike_price_3_val = request.POST.get('strike_price3')
			log_time = request.POST.get('log_time')
			first_history = request.POST.get('first_history')
			
			if first_history == "Yes":
				try:
					# histroy_obj = HistoryLog.objects.filter(strike_price__in=[strike_price_1_val, strike_price_2_val, strike_price_3_val], today_date=dt(2022, 2, 11))
					histroy_obj = HistoryLog.objects.filter(strike_price__in=[strike_price_1_val, strike_price_2_val, strike_price_3_val], today_date=date.today())
					
					temp_list = []
					count = 0
					
					for obj in histroy_obj:
						if count == 0:
							temp_dict = {}
							temp_dict['col1'] = obj.today_time
							temp_dict['col8'] = obj.ltp
						temp_dict[f'col{count+2}'] = obj.call_change_oi
						temp_dict[f'col{count+5}'] = obj.put_change_oi
						count = count + 1
						
						if count == 3:
							temp_list.append(temp_dict)
							count = 0

					if histroy_obj:
						return JsonResponse({"status":"1",'data': temp_list }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong' }) 
			else:
				# print(strike_price_1_val, strike_price_2_val, strike_price_3_val)
				# print(log_time)
				
				# print(strike_price_1_val, strike_price_2_val, strike_price_3_val)
				try:
					histroy_obj = HistoryLog.objects.filter(strike_price__in=[strike_price_1_val, strike_price_2_val, strike_price_3_val],today_time__contains=log_time, today_date=date.today())
					
					temp_list = []
					count = 0
					
					for obj in histroy_obj:
						if count == 0:
							temp_dict = {}
							temp_dict['col1'] = obj.today_time
							temp_dict['col8'] = obj.ltp
						temp_dict[f'col{count+2}'] = obj.call_change_oi
						temp_dict[f'col{count+5}'] = obj.put_change_oi
						count = count + 1
						
						if count == 3:
							temp_list.append(temp_dict)
							count = 0

					if histroy_obj:
						return JsonResponse({"status":"1",'data': temp_list })
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong'})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})

@csrf_exempt
def three_strike_oi_analysis_data(request):
	if request.method == 'POST':
		try:
			strike_price_1_val = request.POST.get('strike_price_1')
			strike_price_2_val = request.POST.get('strike_price_2')
			strike_price_3_val = request.POST.get('strike_price_3')
			first_history = request.POST.get('first_history')
			symbol = request.POST.get('symbol')
			check_date = None;
			if date.today().weekday() == 5:
				check_date = date.today() - timedelta(days=1)
			elif date.today().weekday() == 6:
				check_date = date.today() - timedelta(days=2)
			else:
				check_date = date.today()
				
			
			if first_history == "Yes":
				try:
					if symbol == 'Nifty':
						histroy_obj = HistoryLog.objects.filter(strike_price__in=[strike_price_1_val, strike_price_2_val, strike_price_3_val], today_date=check_date)
					else:
						histroy_obj = BnfHistoryLog.objects.filter(strike_price__in=[strike_price_1_val, strike_price_2_val, strike_price_3_val], today_date=check_date)
						
					temp_list = []
					count = 0
					
					for obj in histroy_obj:
						if count == 0:
							temp_dict = {}
							temp_dict['col1'] = obj.today_time
							temp_dict['col8'] = obj.ltp
						temp_dict[f'col{count+2}'] = obj.call_change_oi
						temp_dict[f'col{count+5}'] = obj.put_change_oi
						count = count + 1
						
						if count == 3:
							temp_list.append(temp_dict)
							count = 0

					if histroy_obj:
						return JsonResponse({"status":"1",'data': temp_list }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong' }) 
			else:
				try:
					log_time = request.POST.get('log_time')
					
					if symbol == 'Nifty':
						histroy_obj = HistoryLog.objects.filter(strike_price__in=[strike_price_1_val, strike_price_2_val, strike_price_3_val],today_time__contains=log_time, today_date=check_date)
					else:
						histroy_obj = BnfHistoryLog.objects.filter(strike_price__in=[strike_price_1_val, strike_price_2_val, strike_price_3_val],today_time__contains=log_time, today_date=check_date)
					
					temp_list = []
					count = 0
					
					for obj in histroy_obj:
						if count == 0:
							temp_dict = {}
							temp_dict['col1'] = obj.today_time
							temp_dict['col8'] = obj.ltp
						temp_dict[f'col{count+2}'] = obj.call_change_oi
						temp_dict[f'col{count+5}'] = obj.put_change_oi
						count = count + 1
						
						if count == 3:
							temp_list.append(temp_dict)
							count = 0

					if histroy_obj:
						return JsonResponse({"status":"1",'data': temp_list })
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong'})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def total_change_oi_history_log(request):
	if request.method == 'POST':
		try:
			first_history = request.POST.get('first_history')
			
			if first_history == "Yes":
				try:
					# histroy_obj = SumOfOiLog.objects.filter(today_date=dt(2022, 2, 11)).values()
					histroy_obj = SumOfOiLog.objects.filter(today_date=date.today()).values()

					if histroy_obj:
						return JsonResponse({"status":"1",'data': list(histroy_obj) }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong' }) 
			else:
				# print(strike_price_1_val, strike_price_2_val, strike_price_3_val)
				log_time = request.POST.get('total_log_time')
				
				# print(log_time)
				try:
					histroy_obj = SumOfOiLog.objects.filter(today_date=date.today(), today_time__contains=log_time).values()
					
					if histroy_obj:
						return JsonResponse({"status":"1",'data': list(histroy_obj) }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' })  
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong'})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def get_yesterday_intraday_data_log(request):
	if request.method == 'POST':
		try:
			if date.today().weekday() == 6:
				yesterday_date = date.today() - timedelta(days=2 )
			else:
				yesterday_date = date.today() - timedelta(days=1)
			
			symbol = request.POST.get('symbol')
		
			try:
				histroy_obj = IntradayFutureAnalysis.objects.filter(today_date=yesterday_date, symbol=symbol).values()
				
				if histroy_obj:
					return JsonResponse({"status":"1",'data': list(histroy_obj) }) 
				else:
					return JsonResponse({"status":"0",'msg': 'data not found' }) 
			except:
				traceback.print_exc()
				return JsonResponse({"status":"0",'msg': 'Something went wrong' }) 
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def intraday_data_log(request):
	if request.method == 'POST':
		try:
			first_history = request.POST.get('first_history')
			symbol = request.POST.get('symbol')
			
			if first_history == "Yes":
				try:
					histroy_obj = IntradayFutureAnalysis.objects.filter(today_date=date.today(), symbol=symbol).values()
					
					# print(date.today() - timedelta(days=1)) 
					
					if histroy_obj:
						return JsonResponse({"status":"1",'data': list(histroy_obj) }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong' }) 
			else:
				log_time = request.POST.get('total_log_time')
				
				try:
					histroy_obj = IntradayFutureAnalysis.objects.filter(today_date=date.today(), symbol=symbol, today_time__contains=log_time).values()
					
					if histroy_obj:
						return JsonResponse({"status":"1",'data': list(histroy_obj) }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' })  
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong'})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def option_price_vs_oi_data(request):
	if request.method == 'POST':
		try:
			first_history = request.POST.get('first_history')
			symbol = request.POST.get('symbol')
			strike_price = request.POST.get('strike_price')
			
			if first_history == "Yes":
				try:
					history_obj = None;
					if symbol == 'Nifty':
						histroy_obj = HistoryLog.objects.filter(today_date=date.today(), strike_price=strike_price).values()
					elif symbol == 'BankNifty':
						histroy_obj = BnfHistoryLog.objects.filter(today_date=date.today(), strike_price=strike_price).values()
					
					if histroy_obj:
						return JsonResponse({"status":"1",'data': list(histroy_obj) }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong' }) 
			else:
				log_time = request.POST.get('total_log_time')
				
				try:
					history_obj = None;
					if symbol == 'Nifty':
						histroy_obj = HistoryLog.objects.filter(today_date=date.today(), strike_price=strike_price, today_time__contains=log_time).values()
					elif symbol == 'BankNifty':
						histroy_obj = BnfHistoryLog.objects.filter(today_date=date.today(), strike_price=strike_price, today_time__contains=log_timee).values()
			
					
					if histroy_obj:
						return JsonResponse({"status":"1",'data': list(histroy_obj) }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' })  
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong'})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def oi_chart_data(request):
	if request.method == 'POST':
		try:
			first_history = request.POST.get('first_history')
			symbol = request.POST.get('symbol')
			strike_price_start = request.POST.get('strike_price_start')
			strike_price_end = request.POST.get('strike_price_end')
			day_argument = request.POST.get('day_argument')
			date_selected = request.POST.get('date_selected')
			
			date_converted = datetime.strptime(date_selected, '%Y-%m-%d').date()
			
			if first_history == "Yes":
				if day_argument == 'saturday':
					check_date = date_converted - timedelta(days = 1)
				elif day_argument == 'sunday':
					check_date = date_converted - timedelta(days = 2)
				elif day_argument == 'Monday':
					check_date = date_converted - timedelta(days = 3)
				elif day_argument == 'yesterday':
					check_date = date_converted - timedelta(days = 1)
				elif day_argument == 'today':
					check_date = date_converted
				else:
					check_date == date_converted
					
				try:
					history_obj = None;
					if symbol == 'Nifty':
						histroy_obj = HistoryLog.objects.filter(strike_price__range=[strike_price_start,strike_price_end],today_date=check_date).values()
					elif symbol == 'BankNifty':
						histroy_obj = BnfHistoryLog.objects.filter(strike_price__range=[strike_price_start,strike_price_end],today_date=check_date).values()
					if histroy_obj:
						return JsonResponse({"status":"1",'data': list(histroy_obj) }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong' }) 
			else:
				log_time = request.POST.get('total_log_time')
				
				if day_argument == 'saturday':
					check_date = date_converted - timedelta(days = 1)
				elif day_argument == 'sunday':
					check_date = date_converted - timedelta(days = 2)
				elif day_argument == 'Monday':
					check_date = date_converted - timedelta(days = 3)
				elif day_argument == 'yesterday':
					check_date = date_converted - timedelta(days = 1)
				elif day_argument == 'today':
					check_date = date_converted
				else:
					check_date == date_converted
					
				# print(symbol, strike_price_start, strike_price_end, day_argument, date_selected, log_time)
				try:
					history_obj = None;
					if symbol == 'Nifty':
						histroy_obj = HistoryLog.objects.filter(strike_price__range=[strike_price_start,strike_price_end],today_date=check_date, today_time__contains=log_time).values()
					elif symbol == 'BankNifty':
						histroy_obj = BnfHistoryLog.objects.filter(strike_price__range=[strike_price_start,strike_price_end],today_date=check_date, today_time__contains=log_time).values()
					if histroy_obj:
						return JsonResponse({"status":"1",'data': list(histroy_obj) }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong' }) 
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})

@csrf_exempt
def ten_strike_oi_analysis_data(request):
	if request.method == 'POST':
		try:
			first_history = request.POST.get('first_history')
			symbol = request.POST.get('symbol')
			strike_price_start = request.POST.get('strike_price_1')
			strike_price_end = request.POST.get('strike_price_2')
			
			if first_history == "Yes":
				check_date = None;
				if date.today().weekday() == 5:
					check_date = date.today() - timedelta(days=1)
				elif date.today().weekday() == 6:
					check_date = date.today() - timedelta(days=2)
				else:
					check_date = date.today()
				try:
					history_obj = None;
					if symbol == 'Nifty':
						history_obj = HistoryLog.objects.values('today_time__hour','today_time__minute').filter(strike_price__range=[strike_price_start,strike_price_end],today_date=check_date).annotate(call_oi_sum=Sum('call_oi'),put_oi_sum=Sum('put_oi'))
					elif symbol == 'BankNifty':
						history_obj = BnfHistoryLog.objects.values('today_time__hour','today_time__minute').filter(strike_price__range=[strike_price_start,strike_price_end],today_date=check_date).annotate(call_oi_sum=Sum('call_oi'),put_oi_sum=Sum('put_oi'))
					if history_obj:
						return JsonResponse({"status":"1",'data': list(history_obj)}) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong' }) 
			else:
				log_time = request.POST.get('total_log_time')
				
				check_date = None;
				if date.today().weekday() == 5:
					check_date = date.today() - timedelta(days=1)
				elif date.today().weekday() == 6:
					check_date = date.today() - timedelta(days=2)
				else:
					check_date = date.today()
				try:
					history_obj = None;
					if symbol == 'Nifty':
						# histroy_obj = HistoryLog.objects.filter(strike_price__range=[strike_price_start,strike_price_end],today_date=check_date, today_time__contains=log_time).values()
						history_obj = HistoryLog.objects.values('today_time__hour','today_time__minute').filter(strike_price__range=[strike_price_start,strike_price_end],today_date=check_date, today_time__contains=log_time).annotate(call_oi_sum=Sum('call_oi'),put_oi_sum=Sum('put_oi'))
					elif symbol == 'BankNifty':
						# histroy_obj = BnfHistoryLog.objects.filter(strike_price__range=[strike_price_start,strike_price_end],today_date=check_date, today_time__contains=log_time).values()
						history_obj = BnfHistoryLog.objects.values('today_time__hour','today_time__minute').filter(strike_price__range=[strike_price_start,strike_price_end],today_date=check_date, today_time__contains=log_time).annotate(call_oi_sum=Sum('call_oi'),put_oi_sum=Sum('put_oi'))
					
					if history_obj:
						return JsonResponse({"status":"1",'data': list(history_obj) }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong' }) 
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def set_nifty_sentiments(request):
	if request.method == 'POST':
		sentiment = request.POST.get('sentiment')
		sentiment_type = request.POST.get('sentiment_type')
		user_id = request.POST.get('user_id')
		symbol = request.POST.get('type')
		
		if symbol == 'Nifty':
			try:
				user_obj = UserDetails.objects.get(id=user_id)
				try:
					if sentiment_type == 'fil':
						update_obj = NiftySentiments.objects.filter(user=user_obj).update(fil=sentiment)
					elif sentiment_type == 'oi':
						update_obj = NiftySentiments.objects.filter(user=user_obj).update(oi=sentiment)
					elif sentiment_type == 'sgx':
						update_obj = NiftySentiments.objects.filter(user=user_obj).update(sgx=sentiment)
					elif sentiment_type == 'preop':
						update_obj = NiftySentiments.objects.filter(user=user_obj).update(preop=sentiment)
					
					if update_obj:
						return JsonResponse({"status":"1",'msg': 'Done'})
					else:
						try:
							if sentiment_type == 'fil':
								NiftySentiments.objects.update_or_create(user=user_obj, fil=sentiment, oi="", sgx="", preop="")
								return JsonResponse({"status":"1",'msg': 'Done'})
							elif sentiment_type == 'oi':
								NiftySentiments.objects.update_or_create(user=user_obj, fil="", oi=sentiment, sgx="", preop="")
								return JsonResponse({"status":"1",'msg': 'Done'})
							elif sentiment_type == 'sgx':
								NiftySentiments.objects.update_or_create(user=user_obj, fil="", oi="", sgx=sentiment, preop="")
								return JsonResponse({"status":"1",'msg': 'Done'})
							elif sentiment_type == 'preop':
								NiftySentiments.objects.update_or_create(user=user_obj, fil="", oi="", sgx="", preop=sentiment)
								return JsonResponse({"status":"1",'msg': 'Done'})
							else:
								return JsonResponse({"status":"0",'msg': 'Something went wrong'})
						except:
							return JsonResponse({"status":"0",'msg': 'Something went wrong'})
				except:
					return JsonResponse({"status":"0",'msg': 'Something went wrong'})
			except:
				return JsonResponse({"status":"0",'msg': 'Something went wrong'})
		elif symbol == 'BankNifty':
			try:
				user_obj = UserDetails.objects.get(id=user_id)
				try:
					if sentiment_type == 'fil':
						update_obj = BankNiftySentiments.objects.filter(user=user_obj).update(fil=sentiment)
					elif sentiment_type == 'oi':
						update_obj = BankNiftySentiments.objects.filter(user=user_obj).update(oi=sentiment)
					elif sentiment_type == 'sgx':
						update_obj = BankNiftySentiments.objects.filter(user=user_obj).update(sgx=sentiment)
					elif sentiment_type == 'preop':
						update_obj = BankNiftySentiments.objects.filter(user=user_obj).update(preop=sentiment)
					
					if update_obj:
						return JsonResponse({"status":"1",'msg': 'Done'})
					else:
						try:
							if sentiment_type == 'fil':
								BankNiftySentiments.objects.update_or_create(user=user_obj, fil=sentiment, oi="", sgx="", preop="")
								return JsonResponse({"status":"1",'msg': 'Done'})
							elif sentiment_type == 'oi':
								BankNiftySentiments.objects.update_or_create(user=user_obj, fil="", oi=sentiment, sgx="", preop="")
								return JsonResponse({"status":"1",'msg': 'Done'})
							elif sentiment_type == 'sgx':
								BankNiftySentiments.objects.update_or_create(user=user_obj, fil="", oi="", sgx=sentiment, preop="")
								return JsonResponse({"status":"1",'msg': 'Done'})
							elif sentiment_type == 'preop':
								BankNiftySentiments.objects.update_or_create(user=user_obj, fil="", oi="", sgx="", preop=sentiment)
								return JsonResponse({"status":"1",'msg': 'Done'})
							else:
								return JsonResponse({"status":"0",'msg': 'Something went wrong'})
						except:
							return JsonResponse({"status":"0",'msg': 'Something went wrong'})
				except:
					return JsonResponse({"status":"0",'msg': 'Something went wrong'})
			except:
				return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
	
######################### BANK NIFTY ######################################

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def bnfGannAnglesDashboard(request):
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---'
			user_obj.current_active_status = 'Inactive'
			
		if user_obj.login_token == login_token:
			return render(request, 'Panel/dashboard-bnf-gann-angles.html',{'user':user_obj})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')
		
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_bank_nifty_dashboard_page(request):	
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---'
			user_obj.current_active_status = 'Inactive'
			
		d = dt.now().date()
		date_list = []
		# d = dt.strptime('2022-02-24', '%Y-%m-%d').date()
		weekday = 3
		
		if (d.weekday() == 3):
			temp_date = f"{int(d.day)} {calendar.month_abbr[int(d.month)]} {int(d.year)}"
			date_list.append(temp_date)
		
		for i in range(6):
			days_ahead = weekday - d.weekday()
			if days_ahead <= 0:
				days_ahead += 7
			next_thursday = d + timedelta(days_ahead)
			
			d = next_thursday
			
			temp_date = f"{int(next_thursday.day)} {calendar.month_abbr[int(next_thursday.month)]} {int(next_thursday.year)}"
			date_list.append(temp_date)
		
		if user_obj.login_token == login_token:
			if BankNiftyHistoryLogInterval.objects.filter(user=user_obj).exists() and BankNiftySentiments.objects.filter(user=user_obj).exists():
				interval_obj = BankNiftyHistoryLogInterval.objects.get(user=user_obj)
				sentiments_obj = BankNiftySentiments.objects.get(user=user_obj)
				
				return render(request, 'Panel/dashboard-bank-nifty.html', {'interval_obj':interval_obj, 'user':user_obj,'page':'banknifty','sentiments_obj':sentiments_obj, 'date_list':date_list})
			else:
				interval_obj = ""
				sentiments_obj = ""
				
				return render(request, 'Panel/dashboard-bank-nifty.html', {'interval_obj':interval_obj, 'user':user_obj,'page':'banknifty','sentiments_obj':sentiments_obj, 'date_list':date_list})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')
		
@csrf_exempt
def set_bank_nifty_user_interval(request):
	if request.method == 'POST':
		interval_val = request.POST.get('interval_val')
		user_id = request.POST.get('user_id')
		
		try:
			user_obj = UserDetails.objects.get(id=user_id)
			
			try:
				update_obj = BankNiftyHistoryLogInterval.objects.filter(user=user_obj).update(interval=interval_val)
				
				if update_obj:
					return JsonResponse({"status":"1",'msg': 'Done'})
				else:
					try:
						BankNiftyHistoryLogInterval.objects.update_or_create(user=user_obj, interval=interval_val, interval_total_oi=3)
						return JsonResponse({"status":"1",'msg': 'Done'})
					except:
						return JsonResponse({"status":"0",'msg': 'Something went wrong'})
			except:
				return JsonResponse({"status":"0",'msg': 'Something went wrong'})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})

@csrf_exempt
def set_user_bank_nifty_total_interval(request):
	if request.method == 'POST':
		interval_val = request.POST.get('interval_val')
		user_id = request.POST.get('user_id')
		
		try:
			user_obj = UserDetails.objects.get(id=user_id)
			try:
				update_obj = BankNiftyHistoryLogInterval.objects.filter(user=user_obj).update(interval_total_oi=interval_val)
				
				if update_obj:
					return JsonResponse({"status":"0",'msg': 'Done'})
				else:
					try:
						BankNiftyHistoryLogInterval.objects.update_or_create(user=user_obj, interval=1, interval_total_oi=interval_val)
						return JsonResponse({"status":"0",'msg': 'Done'})
					except:
						return JsonResponse({"status":"0",'msg': 'Something went wrong'})
			except:
				return JsonResponse({"status":"0",'msg': 'Something went wrong'})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def bnf_history_logging_data(request):
	if request.method == 'POST':
		try:
			strike_price_1_val = request.POST.get('strike_price1')
			strike_price_2_val = request.POST.get('strike_price2')
			strike_price_3_val = request.POST.get('strike_price3')
			log_time = request.POST.get('log_time')
			first_history = request.POST.get('first_history')
			
			if first_history == "Yes":
				try:
					histroy_obj = BnfHistoryLog.objects.filter(strike_price__in=[strike_price_1_val, strike_price_2_val, strike_price_3_val], today_date=date.today())
					
					temp_list = []
					count = 0
					
					for obj in histroy_obj:
						if count == 0:
							temp_dict = {}
							temp_dict['col1'] = obj.today_time
							temp_dict['col8'] = obj.ltp
						temp_dict[f'col{count+2}'] = obj.call_change_oi
						temp_dict[f'col{count+5}'] = obj.put_change_oi
						count = count + 1
						
						if count == 3:
							temp_list.append(temp_dict)
							count = 0

					if histroy_obj:
						return JsonResponse({"status":"1",'data': temp_list }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong' }) 
			else:
				# print(strike_price_1_val, strike_price_2_val, strike_price_3_val)
				# print(log_time)
				
				# print(strike_price_1_val, strike_price_2_val, strike_price_3_val)
				try:
					histroy_obj = BnfHistoryLog.objects.filter(strike_price__in=[strike_price_1_val, strike_price_2_val, strike_price_3_val],today_time__contains=log_time, today_date=date.today())
					
					temp_list = []
					count = 0
					
					for obj in histroy_obj:
						if count == 0:
							temp_dict = {}
							temp_dict['col1'] = obj.today_time
							temp_dict['col8'] = obj.ltp
						temp_dict[f'col{count+2}'] = obj.call_change_oi
						temp_dict[f'col{count+5}'] = obj.put_change_oi
						count = count + 1
						
						if count == 3:
							temp_list.append(temp_dict)
							count = 0

					if histroy_obj:
						return JsonResponse({"status":"1",'data': temp_list })
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong'})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def bnf_total_change_oi_history_log(request):
	if request.method == 'POST':
		try:
			first_history = request.POST.get('first_history')
			
			if first_history == "Yes":
				try:
					# histroy_obj = SumOfOiLog.objects.filter(today_date=dt(2022, 2, 11)).values()
					histroy_obj = BnfSumOfOiLog.objects.filter(today_date=date.today()).values()

					if histroy_obj:
						return JsonResponse({"status":"1",'data': list(histroy_obj) }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' }) 
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong' }) 
			else:
				# print(strike_price_1_val, strike_price_2_val, strike_price_3_val)
				log_time = request.POST.get('total_log_time')
				
				# print(log_time)
				try:
					histroy_obj = BnfSumOfOiLog.objects.filter(today_date=date.today(), today_time__contains=log_time).values()
					
					if histroy_obj:
						return JsonResponse({"status":"1",'data': list(histroy_obj) }) 
					else:
						return JsonResponse({"status":"0",'msg': 'data not found' })  
				except:
					traceback.print_exc()
					return JsonResponse({"status":"0",'msg': 'Something went wrong'})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def bnf_get_open_val(request):
	if request.method == 'POST':
		try:
			open_value = BnfSaveOpenModel.objects.filter(today_date=date.today()).last().open_val
			
			return JsonResponse({"status":"1",'data': open_value})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})


######################### FUNCTIONALITY ######################################

@csrf_exempt
def new_user_signup(request):
	name = request.POST.get('name')
	email = request.POST.get('email')
	password = request.POST.get('password')
	
	if UserDetails.objects.filter(email = email).exists():
		response = "exists"
	else:
		user_obj = UserDetails(name = name, email = email, password = password, user_status = True, approval_status="Pending")
		user_obj.save()
		
		interval_obj = HistoryLogInterval(user = user_obj, interval = 1, interval_total_oi=3)
		interval_obj.save()
		
		bank_interval_obj = BankNiftyHistoryLogInterval(user = user_obj, interval = 1, interval_total_oi=3)
		bank_interval_obj.save()
		
		# IntradayFutureAnalysisInterval(user=user_obj, interval=5).save()
		
		nifty_sentiments = NiftySentiments(user= user_obj, fil="", oi="", sgx="", preop="")
		bnf_nifty_sentiments = BankNiftySentiments(user= user_obj, fil="", oi="", sgx="", preop="")
		
		
		nifty_sentiments.save()
		bnf_nifty_sentiments.save()
		# request.session['user_id'] = user_obj.id
		
		response = "success"
	return HttpResponse(response)

	
@csrf_exempt
def user_login_check(request):
	email = request.POST.get('email')
	password = request.POST.get('password')
	
	if UserDetails.objects.filter(email = email, password = password).exists():
		user_obj = UserDetails.objects.get(email = email, password = password)
		if user_obj.approval_status == 'Approved' or user_obj.approval_status == 'Pending':
			if not user_obj.is_login:
				login_token = "".join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation,25))
				
				user_obj.login_token = login_token
				user_obj.is_login = True
				
				user_obj.save()
				
				request.session['user_id'] = user_obj.id
				request.session['login_token'] = login_token
				response = "successAdmin" 
			else:
				response = "Already Login"
				
		elif user_obj.approval_status == 'Rejected':
			response = "rejected"
		# elif user_obj.approval_status == 'Pending':
			# response = "pending"
	else:
		response = "errorAdmin"
	return HttpResponse(response)
	
@csrf_exempt
def forced_user_log_in(request):
	if request.method == 'POST':
		try:
			email = request.POST.get('email')
			password = request.POST.get('password')
			
			# print(email, password)
			
			if UserDetails.objects.filter(email = email, password = password).exists():
				user_obj = UserDetails.objects.get(email = email, password = password)
				if user_obj.approval_status == 'Approved' or user_obj.approval_status == 'Pending':
					login_token = "".join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation,25))
					
					user_obj.login_token = login_token
					
					user_obj.save()
					
					request.session['user_id'] = user_obj.id
					request.session['login_token'] = login_token
					
					return JsonResponse({"status":"1"}) 
					
				elif user_obj.approval_status == 'Rejected':
					return JsonResponse({"status":"0",'msg': 'rejected'})
				# elif user_obj.approval_status == 'Pending':
					# return JsonResponse({"status":"0",'msg': 'pending'})
			else:
				return JsonResponse({"status":"0",'msg': 'errorAdmin'})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
	
	
	
 ######################### Disconnect API ################################
 
 
@csrf_exempt
def disconnect_truedata_websocket(request):
	try:
		td_app.stop_live_data(symbols)
		td_app.disconnect()
		t1.stop()
		t2.stop()
	except:
		return HttpResponse(str(traceback.format_exc()))
	return HttpResponse('Success')
	
@csrf_exempt
def connect_truedata_websocket(request):
	try:
		td_app.stop_live_data(symbols)
		td_app.disconnect()
		t1.stop()
	except:
		return HttpResponse('Something went wrong')
	return HttpResponse('Success')
 
@csrf_exempt
def delete_history_logs(request):
	try:
		history_records = HistoryLog.objects.all()
		history_records.delete()
	except:
		return HttpResponse('Something went wrong')
	return HttpResponse('Deleted')
	
 ########################################################################
 
 
 
 
 
 
 ##################################### Admin Panel ######################################
 
def adminDashboard(request):
	user_id = request.session.get("admin_user_id")
	if user_id:
		# user_obj = AdminUser.objects.get(id=user_id)
		return render(request, 'AdminPanel/admin-dashboard.html')
	else:
		return redirect('/adminLogin/')
	
	
def adminLogin(request):
	if request.session.get("admin_user_id"):
		del request.session['admin_user_id']
	return render(request, 'AdminPanel/adminLogin.html')
	
@csrf_exempt
def admin_login_check(request):
	email = request.POST.get('email')
	password = request.POST.get('password')
	
	if AdminUser.objects.filter(email = email, password = password).exists():
		request.session['admin_user_id'] = AdminUser.objects.get(email = email, password = password).id
		response = "successAdmin" 
	else:
		response = "errorAdmin"
	return HttpResponse(response)
	
def usersList(request):
	user_id = request.session.get("admin_user_id")
	if user_id:
		# user_obj = AdminUser.objects.get(id=user_id)
		status = ""
		
		users_obj = UserDetails.objects.filter(approval_status="Pending").order_by('-id')
		
		for user in users_obj:
			users_transaction_obj = Transaction.objects.filter(user=user, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
			
			if users_transaction_obj:
				user.sub_start_date = users_transaction_obj.start_date
				user.sub_end_date = users_transaction_obj.end_date
				user.sub_plan_type = users_transaction_obj.plan_type
			else:
				user.sub_start_date = None
				user.sub_end_date = None
				user.sub_plan_type = None 
		
		string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_users_list.html', {'users': users_obj})
		
		admin_obj = AdminUser.objects.get(id=user_id)
		
		# return JsonResponse({"status":"1","smg":"User Added Successfully",'string':string})
		
		subscription_plans_obj = Subscription_Plan.objects.filter(status='Active')
		
		return render(request, 'AdminPanel/users-list.html', {'string':string, 'status':status, 'user': admin_obj,'subscription_plans_obj':subscription_plans_obj})
	else:
		return redirect('/adminLogin/')
		
def add_market_close_dates(request):
	user_id = request.session.get("admin_user_id")
	if user_id:
		dates = MarketWeekOfDate.objects.all().order_by('off_date')
		string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_market_close_dates.html', {'dates': dates})
		return render(request, 'AdminPanel/add_market_close_dates.html',{'string':string})
	else:
		return redirect('/adminLogin/')
		
def adminLogout(request):
	if request.session.get("admin_user_id"):
		del request.session['admin_user_id']
	return redirect('/adminLogin/')
	
@csrf_exempt
def change_user_approval_status(request):
	if request.method == 'POST':
		try:
			status = request.POST.get('status')
			user_id = request.POST.get('user_id')
			filter_status = request.POST.get('filter_status')
			
			updated_obj = UserDetails.objects.filter(id=user_id).update(approval_status=status)
			
			if updated_obj:
				if filter_status == "All": 
					users_obj = UserDetails.objects.all().order_by('-id')
					
				else:
					users_obj = UserDetails.objects.filter(approval_status=filter_status).order_by('-id')
					
				for user in users_obj:
					users_transaction_obj = Transaction.objects.filter(user=user, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
					
					if users_transaction_obj:
						user.sub_start_date = users_transaction_obj.start_date
						user.sub_end_date = users_transaction_obj.end_date
						user.sub_plan_type = users_transaction_obj.plan_type
					else:
						user.sub_start_date = None
						user.sub_end_date = None
						user.sub_plan_type = None
						
				string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_users_list.html', {'users': users_obj})
				
				return JsonResponse({"status":"1",'msg': 'Status updated successfully', 'string': string})
			
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def user_list_filter(request):
	if request.method == 'POST':
		try:
			status = request.POST.get('status')
			
			if status == "All":
				users_obj = UserDetails.objects.all().order_by('-id')
				
				for user in users_obj:
					users_transaction_obj = Transaction.objects.filter(user=user, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
					
					if users_transaction_obj:
						user.sub_start_date = users_transaction_obj.start_date
						user.sub_end_date = users_transaction_obj.end_date
						user.sub_plan_type = users_transaction_obj.plan_type
					else:
						user.sub_start_date = None
						user.sub_end_date = None
						user.sub_plan_type = None
			
				string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_users_list.html', {'users': users_obj})
				
				return JsonResponse({"status":"1",'string': string})
			else:
				users_obj = UserDetails.objects.filter(approval_status=status).order_by('-id')
				
				for user in users_obj:
					users_transaction_obj = Transaction.objects.filter(user=user, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
					
					if users_transaction_obj:
						user.sub_start_date = users_transaction_obj.start_date
						user.sub_end_date = users_transaction_obj.end_date
						user.sub_plan_type = users_transaction_obj.plan_type
					else:
						user.sub_start_date = None
						user.sub_end_date = None
						user.sub_plan_type = None

						
				string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_users_list.html', {'users': users_obj})
				
				return JsonResponse({"status":"1",'string': string})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		


def subscriptionRequest(request):
	user_id = request.session.get("admin_user_id")
	if user_id:
		# user_obj = AdminUser.objects.get(id=user_id)
		status = ""
		
		subscriptions = Transaction.objects.filter(status="Pending").order_by('-id')
		# status = "Pending"
		
		# if not users_obj:
			# users_obj = UserDetails.objects.filter(approval_status="Approved").order_by('-id')
			# status = "Approved"
		
		string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_subscription_request.html', {'subscriptions': subscriptions})
		
		admin_obj = AdminUser.objects.get(id=user_id)
		
		# return JsonResponse({"status":"1","smg":"User Added Successfully",'string':string})
		
		return render(request, 'AdminPanel/subscription_request.html', {'string':string, 'status':status, 'user': admin_obj})
	else:
		return redirect('/adminLogin/')
 
 ##################################### End Admin Panel ######################################
 
 ############################ cash free payment ###############################
 
@csrf_exempt
def set_buy_session(request):
	if request.method == 'POST':
		try:
			request.session['buy_arg'] = 'Buy'
			
			return JsonResponse({"status":"1",'msg': 'Done'})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def delete_buy_session(request):
	if request.method == 'POST':
		try:
			del request.session['buy_arg']
			
			return JsonResponse({"status":"1",'msg': 'Done'})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
 
@csrf_exempt
def test_cash_free_payment(request): 
	if request.method == 'POST':
		url = "https://sandbox.cashfree.com/pg/orders"	  # testing url
		# url = "https://api.cashfree.com/pg/orders"		# production url
		
		try:
			order_id = f"order_id_{''.join(random.sample(string.ascii_lowercase + string.digits,30))}"
			order_amount = request.POST.get('plan_price')
			plan_type = request.POST.get('plan_type')
			plan_id = request.POST.get('plan_id')
			user_id = request.POST.get('user_id')
			start_date = request.POST.get('start_date')
			end_date = request.POST.get('end_date')
			
			user_obj = UserDetails.objects.get(id=user_id)
			subscription_obj = Subscription_Plan.objects.get(id=plan_id)
			payment_type = 'CashFree'
			
			payload = {
				"order_id": order_id,
				"order_amount": order_amount,
				"order_currency": "INR",
				"customer_details": {
					"customer_id": user_id,
					"customer_email": user_obj.email,
					"customer_name": user_obj.name,
					"customer_phone": '0000000000',
				},
				"order_meta": {
					# "return_url":"https://genianalysis.com/payment_success_url/?order_id={order_id}&order_token={order_token}",
					"return_url":"http://172.105.57.86:8040/payment_success_url/?order_id={order_id}&order_token={order_token}",
					"notify_url":"",
				},
				"order_note": plan_type,
			}
			headers = {
				"Accept": "application/json",
				"x-api-version": "2022-01-01",
				"x-client-id": credentials.cashfree_development_appId,
				"x-client-secret" : credentials.cashfree_development_secretKey,
				# "x-client-id": credentials.cashfree_production_appId,
				# "x-client-secret" : credentials.cashfree_production_secretKey,
				"Content-Type": "application/json"
			}

			response = requests.request("POST", url, json=payload, headers=headers)
			
			if response.status_code == 200:
				cf_order_id = response.json()['cf_order_id']
				order_token = response.json()['order_token']
				order_status = response.json()['order_status']
				payment_link = response.json()['payment_link']
				refund_link = response.json()['refunds']['url']
				
				if start_date != 'None' and end_date != 'None':
					Transaction.objects.create(user=user_obj, date_time=timezone.now(), plan_type=plan_type, fk_subscription_plan=subscription_obj, payment_type=payment_type, order_id=order_id, cf_order_id=cf_order_id, order_token=order_token, order_amount=order_amount, order_status=order_status,payment_link=payment_link,refund_link=refund_link, start_date=start_date, end_date=end_date)
					request.session['page_to_redirect'] = 'user_history_page'
				else:
					request.session['page_to_redirect'] = 'home_page'
					Transaction.objects.create(user=user_obj, date_time=timezone.now(), plan_type=plan_type, fk_subscription_plan=subscription_obj, payment_type=payment_type, order_id=order_id, cf_order_id=cf_order_id, order_token=order_token, order_amount=order_amount, order_status=order_status,payment_link=payment_link,refund_link=refund_link)
				
				request.session['current_order_id'] = order_id
				request.session['current_order_token'] = order_token
				
				return JsonResponse({"status":"1",'msg': payment_link})
			else:
				print(response.text)
				return JsonResponse({"status":"0",'msg': 'Something went wrong'})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
@csrf_exempt
def payment_success_url(request):
	if request.method=="GET":
		user_id = request.session.get("user_id")
		user_obj = UserDetails.objects.get(id=user_id)
		print(user_obj)
		order_id = request.GET.get('order_id')
		order_token = request.GET.get('order_token')
		
		session_order_id = request.session.get('current_order_id')
		session_order_token = request.session.get('current_order_token')
		page_to_redirect = request.session.get('page_to_redirect')
		
		if (order_id == session_order_id and order_token == session_order_token):
			# check the order status in the system
			if Transaction.objects.filter(order_id=order_id, order_token=order_token).exists():
				order_obj = Transaction.objects.filter(order_id=order_id, order_token=order_token).last()
				
				if order_obj.order_status == 'PAID':
					request.session['payment_status'] = 'success'
					return redirect('/#criptocurrency-price-section')
				else:
					url = f"https://sandbox.cashfree.com/pg/orders/{session_order_id}" # testing
					
					# url = f"https://api.cashfree.com/pg/orders/{session_order_id}"

					headers = {
						"Accept": "application/json",
						"x-client-id": credentials.cashfree_development_appId,
						"x-client-secret": credentials.cashfree_development_secretKey,
						# "x-client-id": credentials.cashfree_production_appId,
						# "x-client-secret" : credentials.cashfree_production_secretKey,
						"x-api-version": "2022-01-01"
					}

					response = requests.request("GET", url, headers=headers)

					if response.status_code == 200:
						order_status = response.json()['order_status']
						customer_id = response.json()['customer_details']['customer_id']
						
						if order_status == 'PAID':
							try:
								approval_date = date.today()
								user_obj = UserDetails.objects.get(id=customer_id)
								transaction_obj = Transaction.objects.filter(user=user_obj,order_id=order_id, order_token=order_token).last()
								users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=approval_date, end_date__gte=approval_date, status='Approved').last()
								
								if transaction_obj.start_date and transaction_obj.end_date:
									transaction_obj.order_status = 'PAID'
									transaction_obj.status = 'Approved'
									transaction_obj.save()
									
									subject = "Thank you for your purchase!"
									string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_cashfree_success_message.html',{'user_name':user_obj.name})
									to_email = user_obj.email
									email_status = send_email(subject, string, to_email)
									# print(to_email, email_status)
									
									request.session['payment_status'] = 'success'
								elif users_transaction_obj:
									approval_date = users_transaction_obj.end_date
									
									transaction_obj.start_date = approval_date
									
									if transaction_obj.plan_type == 'Monthly':
										 transaction_obj.end_date = approval_date  + relativedelta(months=1)
									elif transaction_obj.plan_type == 'Yearly':
										transaction_obj.end_date = approval_date  + relativedelta(months=12)
									
									transaction_obj.order_status = 'PAID'
									transaction_obj.status = 'Approved'
									transaction_obj.save()
									
									subject = "Thank you for your purchase!"
									string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_cashfree_success_message.html',{'user_name':user_obj.name})
									to_email = user_obj.email
									email_status = send_email(subject, string, to_email)
									# print(to_email, email_status)
									
									request.session['payment_status'] = 'success'
								else:
									transaction_obj.start_date = approval_date
									
									if transaction_obj.plan_type == 'Monthly':
										 transaction_obj.end_date = approval_date  + relativedelta(months=1)
									elif transaction_obj.plan_type == 'Yearly':
										transaction_obj.end_date = approval_date  + relativedelta(months=12)
									
									transaction_obj.order_status = 'PAID'
									transaction_obj.status = 'Approved'
									transaction_obj.save()
									
									subject = "Thank you for your purchase!" 
									string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_cashfree_success_message.html',{'user_name':user_obj.name})
									to_email = user_obj.email
									email_status = send_email(subject, string, to_email)
									# print(to_email, email_status)
									
									request.session['payment_status'] = 'success'
							except:
								subject = "Oh Oh! Your Payment Has Not Been Verified."
								string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_payment_rejected.html',{'user_name':user_obj.name})
								to_email = user_obj.email
								email_status = send_email(subject, string, to_email)
								
								request.session['payment_status'] = 'failed'
						else:
							user_obj = UserDetails.objects.get(id=customer_id)
							transaction_obj = Transaction.objects.filter(user=user_obj,order_id=order_id, order_token=order_token).last()
							transaction_obj.status = 'Failed'
							transaction_obj.save()
							
							subject = "Oh Oh! Your Payment Has Not Been Verified."
							string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_payment_rejected.html',{'user_name':user_obj.name})
							to_email = user_obj.email
							email_status = send_email(subject, string, to_email)
							
							request.session['payment_status'] = 'failed'
						if page_to_redirect == 'home_page':
							return redirect('/#criptocurrency-price-section')
						elif page_to_redirect == 'user_history_page':
							return redirect('/user_subscription_history/')
						else:
							return redirect('/#criptocurrency-price-section')
					else:
						request.session['payment_status'] = 'failed'
						if page_to_redirect == 'home_page':
							return redirect('/#criptocurrency-price-section')
						elif page_to_redirect == 'user_history_page':
							return redirect('/user_subscription_history/')
						else: 
							return redirect('/#criptocurrency-price-section')
			else:
				subject = "Oh Oh! Your Payment Has Not Been Verified."
				string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_payment_rejected.html',{'user_name':user_obj.name})
				to_email = user_obj.email
				email_status = send_email(subject, string, to_email)
				request.session['payment_status'] = 'failed'
				if page_to_redirect == 'home_page':
					return redirect('/#criptocurrency-price-section')
				elif page_to_redirect == 'user_history_page':
					return redirect('/user_subscription_history/')
				else:
					return redirect('/#criptocurrency-price-section')
		else:
			subject = "Oh Oh! Your Payment Has Not Been Verified."
			string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_payment_rejected.html',{'user_name':user_obj.name})
			to_email = user_obj.email
			email_status = send_email(subject, string, to_email)
			request.session['payment_status'] = 'failed'
			if page_to_redirect == 'home_page':
				return redirect('/#criptocurrency-price-section')
			elif page_to_redirect == 'user_history_page':
				return redirect('/user_subscription_history/')
			else:
				return redirect('/#criptocurrency-price-section')
		
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_payment_session(request):
	if request.method == 'POST':
		try:
			del request.session['payment_status']
			del request.session['current_order_id']
			del request.session['current_order_token']
			del request.session['page_to_redirect']
			
			return JsonResponse({"status":"1",'msg': 'Done'})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})

@csrf_exempt
def buy_subscription_dbt(request):
	if request.method=="POST":
		user_id= request.POST.get('user_id')
		plan_type= request.POST.get('plan_type')
		plan_id = request.POST.get('plan_id')
		payment_type = request.POST.get('payment_type')
		receipt = request.FILES.get('receipt')

		user_obj = UserDetails.objects.get(id=user_id)
		subscription_obj = Subscription_Plan.objects.get(id=plan_id)
		
		try:
			Transaction.objects.create(user=user_obj, date_time=timezone.now(), plan_type=plan_type, fk_subscription_plan=subscription_obj, payment_type=payment_type, receipt=receipt)
			subject = "Thank you for your purchase!"
			string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_success_message.html',{'user_name':user_obj.name})
			to_email = user_obj.email
			email_status = send_email(subject, string, to_email)
			return JsonResponse({"status":"1","smg":"Your payment is under review"})
		except:
			subject = "Oh Oh! Your Payment Has Not Been Verified."
			string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_payment_rejected.html',{'user_name':user_obj.name})
			to_email = user_obj.email
			email_status = send_email(subject, string, to_email)
			return JsonResponse({"status":"0","smg":"Something Went Wrong"})
	else:		 
		return JsonResponse({"status":"0","smg":"Post Method Is Req."})

@csrf_exempt
def renew_subscription_by_dbt(request):
	if request.method=="POST":
		user_id= request.POST.get('user_id')
		plan_type= request.POST.get('plan_type')
		plan_id = request.POST.get('plan_id')
		payment_type = request.POST.get('payment_type')
		start_date = request.POST.get('start_date')
		end_date = request.POST.get('end_date')
		receipt = request.FILES.get('receipt')

		# print(user_id, plan_type, plan_id, payment_type, receipt)

		user_obj = UserDetails.objects.get(id=user_id)
		subscription_obj = Subscription_Plan.objects.get(id=plan_id)
		
		try:
			Transaction.objects.create(user=user_obj, date_time=timezone.now(), plan_type=plan_type, fk_subscription_plan=subscription_obj, payment_type=payment_type, receipt=receipt, start_date=start_date, end_date=end_date)
			string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_success_message.html',{'user_name':user_obj.name})
			to_email = user_obj.email
			email_status = send_email(subject, string, to_email)
			return JsonResponse({"status":"1","smg":"Your payment is under review"})
			history_obj = Transaction.objects.filter(user=user_obj).order_by('-date_time')
			string = render_to_string('Panel/r_t_s_Panel/r_t_s_user_subscripion_history.html', {'history_obj': history_obj})
			
			return JsonResponse({"status":"1","smg":"Your payment is under review",'string':string})
		except:
			return JsonResponse({"status":"0","smg":"Something Went Wrong"})
	else:		 
		return JsonResponse({"status":"0","smg":"Post Method Is Req."})
		
@csrf_exempt
def add_manual_subscription(request):
	if request.method=="POST":
		user_id= request.POST.get('user_id')
		plan_type= request.POST.get('plan_type')
		payment_type = 'Manual'
		s_date = request.POST.get('s_date')
		e_date = request.POST.get('e_date')
		filter_status = request.POST.get('filter_status')

		user_obj = UserDetails.objects.get(id=user_id)
		subscription_obj = Subscription_Plan.objects.filter(subscription_type=plan_type, status='Active').last()
		
		try:
			transaction_obj = Transaction.objects.create(user=user_obj, date_time=timezone.now(), plan_type=plan_type, fk_subscription_plan=subscription_obj, payment_type=payment_type, start_date=s_date, end_date=e_date, status="Approved")
			
			if filter_status == "All": 
				users_obj = UserDetails.objects.all().order_by('-id')
			else:
				users_obj = UserDetails.objects.filter(status=filter_status).order_by('-id')
			
			for user in users_obj:
				users_transaction_obj = Transaction.objects.filter(user=user, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
				
				if users_transaction_obj:
					user.sub_start_date = users_transaction_obj.start_date
					user.sub_end_date = users_transaction_obj.end_date
					user.sub_plan_type = users_transaction_obj.plan_type
				else:
					user.sub_start_date = None
					user.sub_end_date = None
					user.sub_plan_type = None

			if plan_type == 'Trial':
				subject = "Trial Activated."
				string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_trial_pack_activate.html',{'user_name':user_obj.name})
				to_email = user_obj.email
				email_status = send_email(subject, string, to_email)

			string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_users_list.html', {'users': users_obj})
			
			return JsonResponse({"status":"1",'msg': 'Subscription Added Successfully','string':string})
				
		except:
			return JsonResponse({"status":"0","smg":"Something Went Wrong"})
	else:		 
		return JsonResponse({"status":"0","smg":"Post Method Is Req."})

@csrf_exempt
def manual_add_market_close_dates(request):
	if request.method=="POST":
		try:
			date_to_add = request.POST.get('date')
			date_converted = datetime.strptime(date_to_add, '%Y-%m-%d').date()
			
			if not MarketWeekOfDate.objects.filter(off_date=date_converted).exists():
				MarketWeekOfDate.objects.create(off_date=date_converted)
				dates = MarketWeekOfDate.objects.all().order_by('off_date')
				string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_market_close_dates.html', {'dates': dates})
				return JsonResponse({"status":"1",'msg': 'Date Added Successfully','string':string})
			else:
				return JsonResponse({"status":"0","smg":"Selected date is already saved in the database"})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0","smg":"Something Went Wrong"})
	else:		 
		traceback.print_exc()
		return JsonResponse({"status":"0","smg":"Post Method Is Req."})

@csrf_exempt
def delete_market_close_dates(request):
	if request.method=="POST":
		try:
			date_id = request.POST.get('id')
			try:
				MarketWeekOfDate.objects.filter(id=date_id).delete()
				dates = MarketWeekOfDate.objects.all().order_by('off_date')
				string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_market_close_dates.html', {'dates': dates})
				return JsonResponse({"status":"1",'msg': 'Date Deleted Successfully','string':string})
			except:
				return JsonResponse({"status":"0","smg":"Something Went Wrong"})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0","smg":"Something Went Wrong"})
	else:		 
		traceback.print_exc()
		return JsonResponse({"status":"0","smg":"Post Method Is Req."})
		
@csrf_exempt
def check_thursday(request):
	if request.method=="POST":
		try:
			date = request.POST.get('date')
			if not MarketWeekOfDate.objects.filter(off_date=date_converted).exists():
				return JsonResponse({"status":"1",'msg': 'market not closed'})
			else:
				return JsonResponse({"status":"1","msg":"market is closed"})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0","smg":"Something Went Wrong"})
	else:		 
		traceback.print_exc()
		return JsonResponse({"status":"0","smg":"Post Method Is Req."})
	
@csrf_exempt
def change_payment_status(request):
	if request.method == 'POST':
		trans_id = request.POST.get('subscription_id')
		status = request.POST.get('status')
		filter_status = request.POST.get('filter_status')
		try:
			transaction_obj = Transaction.objects.filter(id=trans_id).last()
			user_obj = transaction_obj.user
			if status == 'Approved':
				approval_date = date.today()
				
				transaction_obj = Transaction.objects.filter(id=trans_id).last()
				user_obj = transaction_obj.user
				if transaction_obj.start_date and transaction_obj.end_date:
					transaction_obj.status = 'Approved'
					transaction_obj.save()
					
					if filter_status == "All": 
						# transaction_filter_object = Transaction.objects.all().order_by('-id')
						transaction_filter_object = Transaction.objects.exclude(status='Failed').order_by('-id')
					else:
						transaction_filter_object = Transaction.objects.filter(status=filter_status).order_by('-id')
						
					string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_subscription_request.html', {'subscriptions': transaction_filter_object})
					
					subject = "Congratulations! Your Payment Has Been Verified."
					string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_payment_verified.html',{'user_name':user_obj.name})
					to_email = user_obj.email
					email_status = send_email(subject, string, to_email)
					
					return JsonResponse({"status":"1",'msg': 'Payment Approved Successfully','string':string})
				else:
					users_transaction_obj = Transaction.objects.filter(user=transaction_obj.user, start_date__lte=approval_date, end_date__gte=approval_date, status='Approved').last()
					
					if users_transaction_obj:
						approval_date = users_transaction_obj.end_date
						
						transaction_obj.start_date = approval_date
						
						if transaction_obj.plan_type == 'Monthly':
							 transaction_obj.end_date = approval_date  + relativedelta(months=1)
						elif transaction_obj.plan_type == 'Yearly':
							transaction_obj.end_date = approval_date  + relativedelta(months=12)
						
						
						transaction_obj.status = 'Approved'
						transaction_obj.save()
						
						subject = "Congratulations! Your Payment Has Been Verified."
						string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_payment_verified.html',{'user_name':user_obj.name})
						to_email = user_obj.email
						email_status = send_email(subject, string, to_email)
						
						if filter_status == "All": 
							# transaction_filter_object = Transaction.objects.all().order_by('-id')
							transaction_filter_object = Transaction.objects.exclude(status='Failed').order_by('-id')
						else:
							transaction_filter_object = Transaction.objects.filter(status=filter_status).order_by('-id')
							
						string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_subscription_request.html', {'subscriptions': transaction_filter_object})
						
						return JsonResponse({"status":"1",'msg': 'Payment Approved Successfully','string':string})
					else:
						transaction_obj.start_date = approval_date
						
						if transaction_obj.plan_type == 'Monthly':
							 transaction_obj.end_date = approval_date  + relativedelta(months=1)
						elif transaction_obj.plan_type == 'Yearly':
							transaction_obj.end_date = approval_date  + relativedelta(months=12)
						
						transaction_obj.status = 'Approved'
						transaction_obj.save()
						
						subject = "Congratulations! Your Payment Has Been Verified."
						string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_payment_verified.html',{'user_name':user_obj.name})
						to_email = user_obj.email
						email_status = send_email(subject, string, to_email)

						
						if filter_status == "All": 
							# transaction_filter_object = Transaction.objects.all().order_by('-id')
							transaction_filter_object = Transaction.objects.exclude(status='Failed').order_by('-id')
						else:
							transaction_filter_object = Transaction.objects.filter(status=filter_status).order_by('-id')
							
						string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_subscription_request.html', {'subscriptions': transaction_filter_object})
						
						return JsonResponse({"status":"1",'msg': 'Payment Approved Successfully','string':string})

			elif status == 'Rejected':
				transaction_obj = Transaction.objects.filter(id=trans_id).last()
				transaction_obj.status = 'Rejected'
				transaction_obj.save()
				
				subject = "Oh Oh! Your Payment Has Not Been Verified."
				string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_payment_rejected.html',{'user_name':user_obj.name})
				to_email = user_obj.email
				email_status = send_email(subject, string, to_email)
				
				if filter_status == "All": 
					# transaction_filter_object = Transaction.objects.all().order_by('-id')
					transaction_filter_object = Transaction.objects.exclude(status='Failed').order_by('-id')
				else:
					transaction_filter_object = Transaction.objects.filter(status=filter_status).order_by('-id')
					
				string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_subscription_request.html', {'subscriptions': transaction_filter_object})
				
				return JsonResponse({"status":"1",'msg': 'Payment Rejected Successfully', 'string':string})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'}) 
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
		
@csrf_exempt
def transaction_filter(request):
	if request.method == 'POST':
		try:
			status = request.POST.get('status')
			filter_type = request.POST.get('filter_type')
			
			if filter_type == 'with_date':
				from_date = request.POST.get('from_date')
				to_date = request.POST.get('to_date')
				 
				if status == "All":
					to_date = datetime.strptime(to_date , '%Y-%m-%d')
					to_date =  to_date	+ timedelta(days=1)
					transaction_obj = Transaction.objects.filter(date_time__range=(from_date, to_date)).order_by('-id').exclude(status='Failed')
					string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_subscription_request.html', {'subscriptions': transaction_obj})
					return JsonResponse({"status":"1",'string': string})
				else:
					to_date = datetime.strptime(to_date , '%Y-%m-%d')
					to_date =  to_date	+ timedelta(days=1)
					transaction_obj = Transaction.objects.filter(status=status, date_time__range=(from_date, to_date)).order_by('-id')
					string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_subscription_request.html', {'subscriptions': transaction_obj})
					return JsonResponse({"status":"1",'string': string})
			else:
				if status == "All":
					# transaction_obj = Transaction.objects.all().order_by('-id')
					transaction_obj = Transaction.objects.exclude(status='Failed').order_by('-id')
					
					string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_subscription_request.html', {'subscriptions': transaction_obj})
					
					return JsonResponse({"status":"1",'string': string})
				else:
					transaction_obj = Transaction.objects.filter(status=status).order_by('-id')
					
					# print(transaction_obj)
				
					string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_subscription_request.html', {'subscriptions': transaction_obj})
					
					return JsonResponse({"status":"1",'string': string})
		except:
			traceback.print_exc()
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		
 
 ###############################################################################
 ########################## user subscirtion history ############################
 
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_subscription_history(request):
	user_id = request.session.get("user_id")
	login_token = request.session.get("login_token")
	
	if user_id and login_token:
		user_obj = UserDetails.objects.get(id=user_id)
		users_transaction_obj = Transaction.objects.filter(user=user_obj, start_date__lte=date.today(), end_date__gte=date.today(), status='Approved').last()
		
		if users_transaction_obj:
			user_obj.sub_start_date = users_transaction_obj.start_date
			user_obj.sub_end_date = users_transaction_obj.end_date
			user_obj.current_active_status = 'Active'
		else:
			user_obj.sub_start_date = '---'
			user_obj.sub_end_date = '---'
			user_obj.current_active_status = 'Inactive'
			
		if user_obj.login_token == login_token:
			history_obj = Transaction.objects.filter(user=user_obj).order_by('-date_time')
			monthly_subscription = Subscription_Plan.objects.filter(subscription_type="Monthly", status="Active").last()
			yearly_subscription = Subscription_Plan.objects.filter(subscription_type="Yearly", status="Active").last()
	
			string = render_to_string('Panel/r_t_s_Panel/r_t_s_user_subscripion_history.html', {'history_obj': history_obj})
			
			return render(request, 'Panel/user_subscription_history.html', {'user':user_obj, 'string':string, 'monthly_subscription':monthly_subscription,'yearly_subscription':yearly_subscription})
		else:
			return redirect('/login/')
	else:
		return redirect('/login/')
 
 ###################################################################################
 
def email_template(request):
	# string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_cashfree_success_message.html')
	# string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_success_message.html')
	# string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_payment_verified.html')
	# string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_dbt_payment_rejected.html')
	subject = "Thank you for your purchase!"
	string = render_to_string('AdminPanel/r_t_s_AdminPanel/r_t_s_cashfree_success_message.html',{'user_name':'Manoj Khadse'})
	# to_email = user_obj.email
	to_email = 'yamanbisen6403@gmail.com'
	
	email_status = send_email(subject, string, to_email)
	return HttpResponse(email_status)
	# return render(request, 'AdminPanel/r_t_s_AdminPanel/r_t_s_cashfree_success_message.html')
	
############################# Support Resistence ##################################

@csrf_exempt
def add_Support_Resistence(request):
	if request.method == 'POST':
		try:
			user_id = request.POST.get('user_id')
			strike_price = request.POST.get('strike_price')
			analysis = request.POST.get('analysis')
			
			user_obj = UserDetails.objects.get(id=user_id)
			
			if SupportAndResistence.objects.filter(user=user_obj, strike_price=strike_price).exists():
				temp_obj = SupportAndResistence.objects.filter(user=user_obj, strike_price=strike_price).last()
				temp_obj.analysis = analysis
				temp_obj.save()
				return JsonResponse({'status':'1','msg':'Done'})
			else:
				temp_obj = SupportAndResistence.objects.create(user=user_obj, strike_price=strike_price, analysis=analysis)
				return JsonResponse({'status':'1','msg':'Done'})
		except:
			return JsonResponse({"status":"0",'msg': 'Something went wrong'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})

@csrf_exempt
def get_Support_Resistence(request):
	if request.method == 'POST':
		try:
			user_id = request.POST.get('user_id')
			strike_price = request.POST.get('strike_price')
			
			user_obj = UserDetails.objects.get(id=user_id)
			
			if SupportAndResistence.objects.filter(user=user_obj, strike_price=strike_price).exists():
				temp_obj = SupportAndResistence.objects.filter(user=user_obj, strike_price=strike_price).last()
				return JsonResponse({'status':'1','msg':temp_obj.analysis})
			else:
				return JsonResponse({'status':'1','msg':'tug_of_war'})
		except:
			return JsonResponse({"status":"1",'msg': 'tug_of_war'})
	else:
		return JsonResponse({"status":"0",'msg': 'Post request required'})
		