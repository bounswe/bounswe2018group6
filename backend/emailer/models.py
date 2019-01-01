from django.conf import settings
from django.db import models


class EmailLog(models.Model):
    EMAIL_TYPE_CHOICES = (
        ('A', 'Activate account'),
        ('F', 'Forgot password'),
        ('O', 'Other'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    sender = models.EmailField()
    recipient = models.EmailField()
    success = models.BooleanField()
    category = models.CharField(max_length=1, choices=EMAIL_TYPE_CHOICES, default='O')
    sent_at = models.DateTimeField(auto_now=False, auto_now_add=True)
