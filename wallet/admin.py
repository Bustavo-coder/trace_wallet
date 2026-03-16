from django.contrib import admin

from wallet.models import Wallet, Transaction, Ledger


# Register your models here.
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'balance', 'currency', 'status']
    list_editable = ['status']
    list_per_page = 10


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['amount','transaction_type','transaction_status','sender','receiver','created_at']
    list_per_page = 10

@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ['amount', 'balance_after', 'transaction_type', 'created_at','wallet']
    list_per_page = 10
