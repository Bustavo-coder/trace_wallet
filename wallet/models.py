import uuid

from django.db import models
from traceWallet.settings import AUTH_USER_MODEL
from wallet.utils import generate_reference_id,generate_account_number


# Create your models here.
class Wallet(models.Model):
    CURRENCY_CHOICES = (
    ('NGN',"NAIRA"),
    ('USD','DOLLAR'),
    ('EUR','EURO'),
    )
    WALLET_STATUS = (
    ('FROZEN',"Frozen"),
    ("INACTIVE",'Inactive'),
    ("SUSPENDED",'Suspended'),
    ("ACTIVE",'Active'),
    ("CLOSED","closed"),
    )
    user = models.OneToOneField(AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='wallet')
    #on_delete is saying that when we delete the parent the child must be deleted that models.CASCADE but in system we don't delete manually we do soft delete limiting access to the entity
    wallet_number = models.CharField(max_length=10,unique=True,primary_key=True)
    account_number = models.CharField(max_length= 10, unique=True,default=generate_account_number)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    currency = models.CharField(max_length=3, default='NGN',choices=CURRENCY_CHOICES)
    status = models.CharField(max_length=10, choices=WALLET_STATUS, default='ACTIVE')
    def __str__(self):
        return f"{self.account_number}"

class Transaction(models.Model):
    TRANSACTION_CHOICES = (
    ('DEBIT','Debit'),
    ('CREDIT','Credit')
    )
    TRANSACTION_STATUS = (
    ("PENDING","pending"),
    ("SUCCESSFUL","successful"),
    ("FAILED","failed")
    )
    reference = models.CharField(max_length= 20, default=generate_reference_id)
    amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    transaction_type = models.CharField(choices=TRANSACTION_CHOICES,max_length=100)
    sender = models.ForeignKey(Wallet,on_delete=models.PROTECT,related_name='sender')
    receiver = models.ForeignKey(Wallet,on_delete=models.PROTECT,related_name='receiver')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    idempotency_key = models.UUIDField(unique=True,blank=True,editable=False,default=uuid.uuid4)
    transaction_status = models.CharField(choices=TRANSACTION_STATUS,max_length=100)

    def __str__(self):
        return f"{self.reference}\t{self.amount}"
class Ledger (models.Model):
    TRANSACTION_TYPE = (
    ('CREDIT','Credit'),
        ('DEBIT','Debit'),
    )
    transaction = models.ForeignKey(Transaction,on_delete=models.PROTECT,related_name='transaction')
    amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    balance_after = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    wallet = models.ForeignKey(Wallet,on_delete=models.PROTECT,related_name='ledger')
    transaction_type = models.CharField(choices=TRANSACTION_TYPE,max_length=100)
    created_at = models.DateTimeField(auto_now=True)