from django.urls import path
from django import urls

from wallet.views import transfer_wallet

urlpatterns = [
    path("intertansfer/",transfer_wallet,name="inter/transfer"),
]