from decimal import Decimal

import requests
from rest_framework.decorators import api_view

from traceWallet.settings import PAYSTACK_SECRET_KEY,PAYSTACK_VERIFY_URL,PAYSTACK_INITIATE_URL
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from wallet.models import Wallet, Transaction, Ledger

User = get_user_model()
def initiate_paystack_payment(user,amount):
    print(PAYSTACK_SECRET_KEY,PAYSTACK_VERIFY_URL,PAYSTACK_INITIATE_URL)
    header = {
        'Authorization' :f"Bearer {PAYSTACK_SECRET_KEY}",
        'Content-Type': 'application/json',
    }

    data = {
        "email" : user.email,
        "amount" : int(amount * 100),
        "callback_url" : "http://localhost:8000/wallet/callback/",
        'metadata' : {
            "user_id" :str(user.id),
        }
    }
    response = requests.post(PAYSTACK_INITIATE_URL,
                             headers=header,
                             json=data)
    return response.json()

def verify_paystack_payment(reference):
    header = {
        'Authorization' :f"Bearer {PAYSTACK_SECRET_KEY}",
        'Content-Type': 'application/json',
    }
    url = f'{PAYSTACK_VERIFY_URL}{reference}'
    response = requests.get(url,headers=header)
    return response.json()

def credit_wallet(wallet:Wallet,amount,reference:str):
    amount = Decimal(amount)
    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)
        wallet.balance += amount
        wallet.save(update_fields =["balance"])
        tx = Transaction.objects.create(
            amount=amount,
            sender=wallet,
            receiver=wallet,
            transaction_status="SUCCESS",
            transaction_type="CREDIT",
            reference=reference,
        )
        Ledger.objects.create(
            transaction=tx,
            amount=amount,
            wallet=wallet,
            transaction_type='CREDIT',
            balance_after=wallet.balance,
        )
        Ledger.objects.create(
            transaction=tx,
            amount=amount,
            wallet=wallet,
            transaction_type='DEBIT',
            balance_after=wallet.balance
        )
        return tx
@api_view(['GET'])
def paystack_callback(request):
    reference = request.GET.get("reference")

    if not reference:
        return Response({'error':'reference not Supplied'},status=status.HTTP_400_BAD_REQUEST)

    payment_response = verify_paystack_payment(reference)
    amount = payment_response['data']['amount']
    email = payment_response['data']['customer']['email']
    wallet =Wallet.objects.get(user=User.objects.get(email=email))

    tx = credit_wallet(wallet, amount, reference)
    return Response({
        "reference" : tx.reference,
        "amount" : tx.amount,
        "status" : tx.TRANSACTION_STATUS,
        "created_at" : tx.created_at
    },status.HTTP_200_OK)

