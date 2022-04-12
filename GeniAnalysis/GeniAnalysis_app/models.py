from django.db import models


class AdminUser(models.Model):
		name = models.CharField(max_length = 50,null=True, blank=True)
		email = models.CharField(max_length = 50,null=True, blank=True)
		password = models.CharField(max_length = 100,null=True, blank=True)
		admin_user_status = models.BooleanField(default=False)
		login_user_count = models.IntegerField()
	
	
class UserDetails(models.Model):
		name = models.CharField(max_length = 100,null=True, blank=True)
		email = models.CharField(max_length = 100,null=True, blank=True)
		password = models.CharField(max_length = 100,null=True, blank=True)
		user_status = models.BooleanField(default=False)
		approval_status = models.CharField(max_length = 100, null=True, blank=True) # Pending, Rejected, Approved, 
		is_login = models.BooleanField(default=False) 
		login_token = models.CharField(max_length=100, null=True, blank=True, default="")
		
		subscription_status = models.CharField(max_length=100, blank=True, null=True) # Active/Inactive
		start_date = models.DateField(blank=True, null=True)
		end_date = models.DateField(blank=True, null=True)
		subscription_id = models.CharField(max_length=100, blank=True, null=True)
		# subscription_to_fk = models.ForeignKey(

class HistoryLog(models.Model):
	today_time = models.TimeField(auto_now=True)
	today_date = models.DateField(auto_now=True)
	strike_price = models.CharField(max_length=100, null=True, blank=True)
	call_change_oi = models.CharField(max_length=100, null=True, blank=True)
	put_change_oi = models.CharField(max_length=100, null=True, blank=True)
	ltp = models.CharField(max_length=100, null=True, blank=True, default="")
	call_oi = models.CharField(max_length=100, null=True, blank=True)
	put_oi = models.CharField(max_length=100, null=True, blank=True)
	call_ltp = models.CharField(max_length=100, null=True, blank=True)
	put_ltp = models.CharField(max_length=100, null=True, blank=True)
	
class HistoryLogInterval(models.Model):
	user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
	interval = models.IntegerField()
	interval_total_oi = models.IntegerField()
	
class SumOfOiLog(models.Model):
	today_time = models.TimeField(auto_now=True)
	today_date = models.DateField(auto_now=True)
	total_call_change_oi = models.CharField(max_length=100, null=True, blank=True)
	total_put_change_oi = models.CharField(max_length=100, null=True, blank=True)
	
class SaveOpenModel(models.Model):
	today_date = models.DateField(auto_now=True)
	open_val = models.CharField(max_length=100)

class NiftySentiments(models.Model):
	user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
	fil = models.CharField(max_length=10, blank=True, null=True)
	oi = models.CharField(max_length=10, blank=True, null=True)
	sgx = models.CharField(max_length=10, blank=True, null=True)
	preop = models.CharField(max_length=10, blank=True, null=True)
	
###################### Bank Nifty #############################

class BankNiftyHistoryLogInterval(models.Model):
	user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
	interval = models.IntegerField()
	interval_total_oi = models.IntegerField()
	
class BnfHistoryLog(models.Model):
	today_time = models.TimeField(auto_now=True)
	today_date = models.DateField(auto_now=True)
	strike_price = models.CharField(max_length=100, null=True, blank=True)
	call_change_oi = models.CharField(max_length=100, null=True, blank=True)
	put_change_oi = models.CharField(max_length=100, null=True, blank=True)
	ltp = models.CharField(max_length=100, null=True, blank=True, default="")
	call_oi = models.CharField(max_length=100, null=True, blank=True)
	put_oi = models.CharField(max_length=100, null=True, blank=True)
	call_ltp = models.CharField(max_length=100, null=True, blank=True)
	put_ltp = models.CharField(max_length=100, null=True, blank=True)
	
class BnfSumOfOiLog(models.Model):
	today_time = models.TimeField(auto_now=True)
	today_date = models.DateField(auto_now=True)
	total_call_change_oi = models.CharField(max_length=100, null=True, blank=True)
	total_put_change_oi = models.CharField(max_length=100, null=True, blank=True)
	
class BnfSaveOpenModel(models.Model):
	today_date = models.DateField(auto_now=True)
	open_val = models.CharField(max_length=100)
	
class BankNiftySentiments(models.Model):
	user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
	fil = models.CharField(max_length=10, blank=True, null=True)
	oi = models.CharField(max_length=10, blank=True, null=True)
	sgx = models.CharField(max_length=10, blank=True, null=True)
	preop = models.CharField(max_length=10, blank=True, null=True)
	
###################### Bank Nifty #############################

class GannHighLow(models.Model):
	today_date = models.DateField(auto_now=True)
	high_val = models.CharField(max_length=100)
	low_val = models.CharField(max_length=100)
	
class BnfGannHighLow(models.Model):
	today_date = models.DateField(auto_now=True)
	high_val = models.CharField(max_length=100)
	low_val = models.CharField(max_length=100)
	
class Subscription_Plan(models.Model):
	subscription_type = models.CharField(max_length=100, blank=True, null=True)
	price = models.CharField(max_length=100, blank=True, null=True)
	discount = models.CharField(max_length=100, blank=True, null=True)
	amount = models.CharField(max_length=100, blank=True, null=True)
	payble_amount = models.CharField(max_length=100, blank=True, null=True)
	best_value = models.BooleanField(default=False) 
	extra_discount = models.CharField(max_length=100, blank=True, null=True)
	extra_discount_text = models.CharField(max_length=100, blank=True, null=True)
	status = models.CharField(max_length=100, default="Pending", blank=True, null=True)	 # Pending/Active/Inactive
	subscription_days = models.CharField(max_length=100, blank=True, null=True)
	gst_amount = models.CharField(max_length=100, blank=True, null=True)
	net_amount = models.CharField(max_length=100, blank=True, null=True)
	
class Transaction(models.Model):
	user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
	date_time = models.DateTimeField(blank=True, null=True)
	plan_type = models.CharField(max_length=100, blank=True, null=True)
	fk_subscription_plan = models.ForeignKey(Subscription_Plan, on_delete=models.CASCADE)
	payment_type = models.CharField(max_length=100, blank=True, null=True)
	status = models.CharField(max_length=100, default="Pending", blank=True, null=True) # Pending/Approved/Rejected
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)
	receipt = models.FileField(upload_to ='sub_receipt/')
	
	########## cashfree Fields ########
	
	order_id = models.CharField(max_length=100, blank=True, null=True)
	cf_order_id = models.CharField(max_length=100, blank=True, null=True)
	order_token = models.CharField(max_length=100, blank=True, null=True)
	order_amount = models.CharField(max_length=100, blank=True, null=True)
	order_status = models.CharField(max_length=100, blank=True, null=True)
	payment_link = models.CharField(max_length=100, blank=True, null=True)
	refund_link = models.CharField(max_length=100, blank=True, null=True)

	
########################## GeniMode Status #######################

	
class GeniModeDetails(models.Model):
	genimode_type = models.CharField(max_length=100, blank=True, null=True)		 # Bullish / Bearish
	genimode_strike_price = models.CharField(max_length=100, blank=True, null=True)
	genimode_current_ltp = models.CharField(max_length=100, blank=True, null=True)
	genimode_target = models.CharField(max_length=100, blank=True, null=True)
	genimode_stop_loss = models.CharField(max_length=100, blank=True, null=True)
	today_date = models.DateField(auto_now=True)
	symbol = models.CharField(max_length=100, blank=True, null=True)
	selected_strike_price = models.CharField(max_length=100, blank=True, null=True)
	genimode_target_on = models.BooleanField(default=False)
	genimode_stop_loss_on = models.BooleanField(default=False)
	
########################## Support And Resistence Table Status #######################

class SupportAndResistence(models.Model):
	user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
	strike_price = models.CharField(max_length=100, blank=True, null=True)
	analysis = models.CharField(max_length=100, blank=True, null=True)


########################## Intraday Future OI Analysis ###############################

class IntradayFutureAnalysis(models.Model):
	today_time = models.TimeField(auto_now=True)
	today_date = models.DateField(auto_now=True)
	symbol = models.CharField(max_length=100, null=True, blank=True)
	last_price = models.CharField(max_length=100, null=True, blank=True, default="")
	price_change = models.CharField(max_length=100, null=True, blank=True)
	oi_change = models.CharField(max_length=100, null=True, blank=True)
	oi = models.CharField(max_length=100, null=True, blank=True)
	
class IntradayFutureAnalysisInterval(models.Model):
	user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
	interval = models.IntegerField()
	
class MarketWeekOfDate(models.Model):
	off_date = models.DateField()