from django.urls import path
from django import urls

from wallet.views import transfer_wallet, deposit_wallet

urlpatterns = [
    path("intertansfer/",transfer_wallet,name="inter/transfer"),
    path("deposit/",deposit_wallet,name="deposit")
]