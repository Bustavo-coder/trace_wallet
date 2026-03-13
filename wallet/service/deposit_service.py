from decimal import Decimal
from uuid import UUID

from django.db import transaction

from wallet.models import Wallet, Transaction, Ledger


@transaction.atomic
def deposit(wallet: Wallet, amount,idempotency_key:UUID ):
    amount = Decimal(amount)
    if amount <= 0: raise Exception('Amount cannot be negative')

    tx = Transaction.objects.filter(idempotency_key=idempotency_key).exists()
    if tx:
        raise Exception('Transaction already exists')
    wallet.balance += amount
    wallet.save(update_fields=['balance'])
    transaction = Transaction.objects.create(
        sender=wallet,
        receiver=wallet,
        amount=amount,
        transaction_type='CREDIT',
        transaction_status='SUCCESSFUL',
    )
    Ledger.objects.create(
        transaction=transaction,
        amount=amount,
        wallet=wallet,
        balance_after=wallet.balance,
        transaction_type='CREDIT'
    )

    return transaction
