from wallet.service import create_wallet
from user.service import create_user
from notification.services import create_notification
from django.db import transaction

@transaction.atomic
def create_user_and_wallet(validated_data):
    user = create_user(validated_data)
    wallet = create_wallet(user)
    create_notification(user)
    return user,wallet