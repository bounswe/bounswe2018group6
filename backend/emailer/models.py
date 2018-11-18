from django.conf import settings
from django.db import models


class EmailLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    sender = models.EmailField()
    recipient = models.EmailField()
    success = models.BooleanField()
    sent_at = models.DateTimeField(auto_now=False, auto_now_add=True)
