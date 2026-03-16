from notification.services import create_deposit_notification

from wallet.service.fund_wallet import initiate_paystack_payment
def fund_wallet_onboard(user,amount):
  tx = initiate_paystack_payment(user,amount)
  create_deposit_notification(user,amount)
  return tx