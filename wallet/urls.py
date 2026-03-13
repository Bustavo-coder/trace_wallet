from django.urls import path
from django import urls

from wallet.service.fund_wallet import paystack_callback
from wallet.views import transfer_wallet, deposit_wallet, fund_wallet

urlpatterns = [
    path("intertansfer/",transfer_wallet,name="inter/transfer"),
    path("deposit/",deposit_wallet,name="deposit"),
    path("callback/",paystack_callback,name="callback"),
    path("fund/",fund_wallet,name="fund_wallet"),
]