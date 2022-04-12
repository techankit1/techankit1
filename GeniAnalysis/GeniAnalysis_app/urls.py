from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from . import views_web

urlpatterns = [
		##################### RENDER PAGE URLS ########################
    path('', views.websiteHomePage, name='websiteHomePage'),
    path('login/', views.user_login_page, name='user_login_page'),
    path('forced_user_log_in/', views.forced_user_log_in, name='forced_user_log_in'),
    path('logout_api/', views.logout_api, name='logout_api'),
    path('signup_page/', views.user_signup_page, name='user_signup_page'),
    path('dashboard_page/', views.user_dashboard_page, name='user_dashboard_page'),
    path('nifty_dashboard_page/', views.user_nifty_dashboard_page, name='user_nifty_dashboard_page'),
    path('bank_nifty_dashboard_page/', views.user_bank_nifty_dashboard_page, name='user_bank_nifty_dashboard_page'),
    path('oi_analysis_dashboard/', views.oi_analysis_dashboard, name='oi_analysis_dashboard'),
    path('history_logging_data/', views.history_logging_data, name='history_logging_data'),
    path('total_change_oi_history_log/', views.total_change_oi_history_log, name='total_change_oi_history_log'),
    path('termsAndCondition/', views.termsAndCondition, name='termsAndCondition'),
    path('privacyPolicy/', views.termsAndCondition, name='privacyPolicy'),
    path('disconnect_truedata_websocket/', views.disconnect_truedata_websocket, name='disconnect_truedata_websocket'),
    path('delete_history_logs/', views.delete_history_logs, name='delete_history_logs'),
    path('future_oi_analysis_dashboard/', views.future_oi_analysis_dashboard, name='future_oi_analysis_dashboard'),
    path('future_graph_analysis_dashboard/', views.future_graph_analysis_dashboard, name='future_graph_analysis_dashboard'),
    path('dashboard_intraday_future_oi_analysis/', views.dashboard_intraday_future_oi_analysis, name='dashboard_intraday_future_oi_analysis'),
    path('dashboard_price_vs_oi/', views.dashboard_price_vs_oi, name='dashboard_price_vs_oi'),
    path('dashboard_option_price_vs_oi/', views.dashboard_option_price_vs_oi, name='dashboard_option_price_vs_oi'),
    path('dashboard_oi_chart/', views.dashboard_oi_chart, name='dashboard_oi_chart'),
    path('dashboard_three_strike_oi_analysis/', views.dashboard_three_strike_oi_analysis, name='dashboard_three_strike_oi_analysis'),
    path('dashboard_ten_strike_oi_analysis/', views.dashboard_ten_strike_oi_analysis, name='dashboard_ten_strike_oi_analysis'),
    
    
    path('set_user_interval/', views.set_user_interval, name='set_user_interval'),
    path('set_intraday_interval/', views.set_intraday_interval, name='set_intraday_interval'),
    path('intraday_data_log/', views.intraday_data_log, name='intraday_data_log'),
    path('option_price_vs_oi_data/', views.option_price_vs_oi_data, name='option_price_vs_oi_data'),
    path('oi_chart_data/', views.oi_chart_data, name='oi_chart_data'),
    path('get_yesterday_intraday_data_log/', views.get_yesterday_intraday_data_log, name='get_yesterday_intraday_data_log'),
    path('set_user_total_interval/', views.set_user_total_interval, name='set_user_total_interval'),
    path('get_open_val/', views.get_open_val, name='get_open_val'),
    path('three_strike_oi_analysis_data/', views.three_strike_oi_analysis_data, name='three_strike_oi_analysis_data'),
    path('ten_strike_oi_analysis_data/', views.ten_strike_oi_analysis_data, name='ten_strike_oi_analysis_data'),
    
    path('get_gann_values/', views.get_gann_values, name='get_gann_values'),
    path('gannAnglesDashboard/', views.gannAnglesDashboard, name='gannAnglesDashboard'),
    
    
    path('set_nifty_sentiments/', views.set_nifty_sentiments, name='set_nifty_sentiments'),
    
    
    path('test_cash_free_payment/', views.test_cash_free_payment, name='test_cash_free_payment'),
    path('payment_success_url/', views.payment_success_url, name='payment_success_url'),
    path('delete_payment_session/', views.delete_payment_session, name='delete_payment_session'),
    
    path('set_buy_session/', views.set_buy_session, name='set_buy_session'),
    path('delete_buy_session/', views.delete_buy_session, name='delete_buy_session'),
    
    path('get_active_genimode/', views.get_active_genimode, name='get_active_genimode'),
    path('set_target_stop_loss/', views.set_target_stop_loss, name='set_target_stop_loss'),
    
    
    
    ################################ Bank Nifty Panel ##########################################
    
    path('set_bank_nifty_user_interval/', views.set_bank_nifty_user_interval, name='set_bank_nifty_user_interval'),
    path('bnf_history_logging_data/', views.bnf_history_logging_data, name='bnf_history_logging_data'),
    path('bnf_total_change_oi_history_log/', views.bnf_total_change_oi_history_log, name='bnf_total_change_oi_history_log'),
    path('set_user_bank_nifty_total_interval/', views.set_user_bank_nifty_total_interval, name='set_user_bank_nifty_total_interval'),
    path('bnf_get_open_val/', views.bnf_get_open_val, name='bnf_get_open_val'),
    path('bnfGannAnglesDashboard/', views.bnfGannAnglesDashboard, name='bnfGannAnglesDashboard'),
    
    ################################ Admin Panel ##########################################
    
    path('adminDashboard/', views.adminDashboard, name='adminDashboard'),
    path('adminLogin/', views.adminLogin, name='adminLogin'),
    path('admin_login_check/', views.admin_login_check, name='admin_login_check'),
    path('usersList/', views.usersList, name='usersList'),
    path('change_user_approval_status/', views.change_user_approval_status, name='change_user_approval_status'),
    path('user_list_filter/', views.user_list_filter, name='user_list_filter'),
    path('add_manual_subscription/', views.add_manual_subscription, name='add_manual_subscription'),
    path('user_subscription_history/', views.user_subscription_history, name='user_subscription_history'),
    path('add_market_close_dates/', views.add_market_close_dates, name='add_market_close_dates'),
    path('manual_add_market_close_dates/', views.manual_add_market_close_dates, name='manual_add_market_close_dates'),
    path('delete_market_close_dates/', views.delete_market_close_dates, name='delete_market_close_dates'),
    path('check_thursday/', views.check_thursday, name='check_thursday'),
    
    path('subscriptionRequest/', views.subscriptionRequest, name='subscriptionRequest'),
    
    ################################ Admin Panel ##########################################
		
		##################### FUNCTIONAL PAGE URLS ########################
    path('new_user_signup/', views.new_user_signup, name='new_user_signup'),
    path('user_login_check/', views.user_login_check, name='user_login_check'),
    
    
    ################################ subscription urls ##########################
    path('buy_subscription_dbt/', views.buy_subscription_dbt, name='buy_subscription_dbt'),
    path('renew_subscription_by_dbt/', views.renew_subscription_by_dbt, name='renew_subscription_by_dbt'),
    path('change_payment_status/', views.change_payment_status, name='change_payment_status'),
    path('transaction_filter/', views.transaction_filter, name='transaction_filter'),
    
    path('add_Support_Resistence/', views.add_Support_Resistence, name='add_Support_Resistence'),
    path('get_Support_Resistence/', views.get_Support_Resistence, name='get_Support_Resistence'),
    
    
    
    
    path('send_email/', views.send_email, name='send_email'),
    path('email_template/', views.email_template, name='email_template'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

