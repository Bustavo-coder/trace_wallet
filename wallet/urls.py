from django.urls import path

from wallet.service.fund_wallet import paystack_callback
from wallet.views import transfer_wallet, deposit_wallet, fund_wallet, get_dashboard_data

urlpatterns = [
    path("intertansfer/",transfer_wallet,name="inter/transfer"),
    path("deposit/",deposit_wallet,name="deposit"),
    path("callback/",paystack_callback,name="callback"),
    path("fund/", fund_wallet, name="fund_wallet"),
    path("dashboard/",get_dashboard_data,name="dashboard"),
]