from notification.services import create_deposit_notification

from wallet.service.fund_wallet import initiate_paystack_payment
def fund_wallet(user,amount):
  initiate_paystack_payment(user,amount)
  create_deposit_notification(user,amount)