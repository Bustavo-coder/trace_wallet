from .models import  Wallet
def create_wallet(user):
    Wallet.objects.create(
        user=user,
        wallet_number=user.phone[1:]
    )