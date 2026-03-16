from django.dispatch import receiver

from user.models import User
from wallet.models import Transaction


def get_dashboard(user:User):
    transactions = Transaction.objects.filter(
        sender=user.wallet).order_by('-created_at')[:5]

    return {
    "transactions":transactions,
    "message": f"Hi,{user.first_name}",
    "status":user.wallet.status,
    "currency" : user.wallet.currency,
    "balance" : user.wallet.balance,
    'wallet_number' :user.wallet.wallet_number
    }
