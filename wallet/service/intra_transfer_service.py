from decimal import Decimal

from uuid import UUID

from django.db import transaction

from wallet.models import Wallet, Transaction, Ledger

@transaction.atomic
def intra_transfer(sender:Wallet,receiver:Wallet,amount,idempotency_key:UUID,description:str):
    amount = Decimal(amount)

    if sender.pk == receiver.pk: raise Exception("Cannot Transfer to self")
    if amount > sender.balance : raise Exception("Insufficient Balance")
    existing_tx =  Transaction.objects.filter(idempotency_key=idempotency_key).exists()
    if existing_tx:
        return Transaction.objects.get(idempotency_key=idempotency_key)

    receiver_wallet = Wallet.objects.select_for_update().get(wallet_number=receiver.wallet_number)
    sender_wallet = Wallet.objects.select_for_update().get(wallet_number = sender.wallet_number)

    sender_wallet.balance -= amount
    receiver_wallet.balance += amount
    sender_wallet.save(update_fields=['balance'])
    receiver_wallet.save(update_fields=['balance'])

    _transaction =  Transaction.objects.create(
        sender=sender_wallet,
        receiver=receiver_wallet,
        amount=amount,
        idempotency_key=idempotency_key,
        description=description,
        transaction_type = 'CREDIT',
        transaction_status = 'SUCCESSFUL',
    )

    Ledger.objects.create(
        transaction = _transaction,
        amount = amount,
        wallet=sender,
        balance_after = sender_wallet.balance,
        transaction_type= 'DEBIT'
    )
    Ledger.objects.create(
        transaction=_transaction,
        amount=amount,
        wallet=receiver,
        balance_after=receiver_wallet.balance,
        transaction_type='CREDIT',
    )


    return _transaction
