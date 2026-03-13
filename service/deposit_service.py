from uuid import UUID

from django.db.models.fields import return_None

from wallet.models import Wallet
from wallet.service.deposit_service import deposit
from notification.services import create_deposit_notification


def deposit_service(sender:Wallet,amount,idempotency_key:UUID):
   tx =  deposit(sender,amount,idempotency_key)
   create_transfer_notification(sender.user,amount)
   return tx
