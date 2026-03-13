from uuid import UUID

from wallet.models import Wallet
from wallet.service.intra_transfer_service import intra_transfer
from notification.services import create_transfer_notification

def create_transfer(sender:Wallet,receiver:Wallet,amount,idempotency_key:UUID,description:str):
    tx = intra_transfer(sender,receiver,amount,idempotency_key)
    create_transfer_notification(receiver.user,amount)
    return tx