from django.contrib import admin
from .models import *
from django.contrib.sessions.models import Session


class SessionAdmin(admin.ModelAdmin):
	def _session_data(self, obj):
		return obj.get_decoded()
	list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)

class AdminUserClass(admin.ModelAdmin):
	list_display = ('id', 'name', 'email', 'password', 'admin_user_status','login_user_count')
admin.site.register(AdminUser , AdminUserClass)


class UserDetailsClass(admin.ModelAdmin):
	list_display = ('id','name', 'email', 'password', 'user_status', 'approval_status','is_login','login_token', 'subscription_status','start_date','end_date','subscription_id')
admin.site.register(UserDetails , UserDetailsClass)


@admin.register(HistoryLog)
class HistoryLogAdmin(admin.ModelAdmin):
	list_display = ['id','today_time','today_date','strike_price','call_change_oi','put_change_oi','ltp','call_oi','put_oi','call_ltp','put_ltp']

		
@admin.register(HistoryLogInterval)
class HistoryLogIntervalAdmin(admin.ModelAdmin):
	list_display = ['id','user','interval','interval_total_oi']

@admin.register(SaveOpenModel)
class SaveOpenModelAdmin(admin.ModelAdmin):
	list_display = ['id','today_date','open_val']
	
@admin.register(SumOfOiLog)
class SumOfOiLogAdmin(admin.ModelAdmin):
	list_display = ['id','today_time','today_date','total_call_change_oi','total_put_change_oi']
	
@admin.register(NiftySentiments)
class NiftySentimentsAdmin(admin.ModelAdmin):
	list_display = ['id','user','fil','oi','sgx','preop']

##################### Bank Nifty ##########################

@admin.register(BankNiftySentiments)
class BankNiftySentimentsAdmin(admin.ModelAdmin):
	list_display = ['id','user','fil','oi','sgx','preop']
	
@admin.register(BankNiftyHistoryLogInterval)
class BankNiftyHistoryLogIntervalAdmin(admin.ModelAdmin):
	list_display = ['id','user','interval','interval_total_oi']
	
@admin.register(BnfHistoryLog)
class BnfHistoryLogAdmin(admin.ModelAdmin):
	list_display = ['id','today_time','today_date','strike_price','call_change_oi','put_change_oi','ltp','call_oi','put_oi','call_ltp','put_ltp']

@admin.register(BnfSaveOpenModel)
class BnfSaveOpenModelAdmin(admin.ModelAdmin):
	list_display = ['id','today_date','open_val']
	
@admin.register(BnfSumOfOiLog)
class BnfSumOfOiLogAdmin(admin.ModelAdmin):
	list_display = ['id','today_time','today_date','total_call_change_oi','total_put_change_oi']
	
########################### Gann Angles ###################

@admin.register(GannHighLow)
class GannHighLowAdmin(admin.ModelAdmin):
	list_display = ['id','today_date','high_val','low_val']
	
@admin.register(BnfGannHighLow)
class BnfGannHighLowAdmin(admin.ModelAdmin):
	list_display = ['id','today_date','high_val','low_val']
	
########################## Subscription ###########################

@admin.register(Subscription_Plan)
class Subscription_PlanAdmin(admin.ModelAdmin):
	list_display = ['id','subscription_type','price','discount','amount','extra_discount','extra_discount_text','payble_amount','best_value','status','subscription_days','gst_amount','net_amount']
	
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	list_display = ['id','user','date_time','plan_type','fk_subscription_plan','payment_type','status','receipt','start_date','end_date','order_id','cf_order_id','order_token','order_amount','order_status','payment_link','refund_link']


######################### Geni Mode ##############################

@admin.register(GeniModeDetails)
class GeniModeDetailsAdmin(admin.ModelAdmin):
	list_display = ['genimode_type','genimode_strike_price','genimode_current_ltp','genimode_target','genimode_stop_loss','today_date','symbol','selected_strike_price','genimode_target_on','genimode_stop_loss_on']
	
@admin.register(SupportAndResistence)
class SupportAndResistenceAdmin(admin.ModelAdmin):
	list_display = ['id','user','strike_price','analysis']
    
@admin.register(IntradayFutureAnalysis)
class IntradayFutureAnalysisAdmin(admin.ModelAdmin):
	list_display = ['id','today_time','today_date','symbol','last_price','price_change','oi_change','oi']
    
@admin.register(IntradayFutureAnalysisInterval)
class IntradayFutureAnalysisIntervalAdmin(admin.ModelAdmin):
	list_display = ['id','user','interval']
    
@admin.register(MarketWeekOfDate)
class MarketWeekOfDateAdmin(admin.ModelAdmin):
	list_display = ['id','off_date']