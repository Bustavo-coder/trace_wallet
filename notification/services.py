from django.core.mail import send_mail

from .models import Notification

def create_notification(user):
    notification = Notification.objects.create(
        wallet_number= user.wallet.wallet_number,
        message = f"""Hi {user.first_name}! Welcome to Trace Wallet!
        your wallet number is {user.wallet.wallet_number}
        your alternate wallet number is {user.wallet.account_number}
""",
        event_type = "USER_WALLET_CREATED",

    )
    send_mail(
        subject="welcome to quick pay",
        message=notification.message,
        from_email='',
        recipient_list=[user.email],
        fail_silently=True
    )
    notification.is_read = True
    notification.save()
