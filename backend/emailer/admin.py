from django.contrib import admin

from .models import EmailLog


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'sender', 'recipient', 'category', 'success', 'sent_at')
    readonly_fields = ('id', 'user', 'sender', 'recipient', 'category', 'success', 'sent_at')
    
    ordering = ('-sent_at',)
    list_display = ('id', 'user', 'sender', 'recipient', 'category', 'success', 'sent_at')
