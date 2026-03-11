from django.db import models

import user.models
import wallet
from traceWallet.settings import AUTH_USER_MODEL


# Create your models here.
class Notification(models.Model):
    Notification_TYPE = (
    ("MESSAGE","message"),
    ("EMAIL","email"),
    )
    wallet_number = models.CharField(max_length=100,blank=True,null=True,)
    reference = models.CharField(max_length=40,unique=True,blank=True,null=True)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    channel = models.CharField(max_length=120,choices=Notification_TYPE,default="EMAIL")
    event_type = models.CharField(max_length=50,default="EMAIL")
    is_read = models.BooleanField(default=False)


