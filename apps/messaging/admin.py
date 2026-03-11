from django.contrib import admin

from .models import InquiryMessage


@admin.register(InquiryMessage)
class InquiryMessageAdmin(admin.ModelAdmin):
    list_display = ("listing", "sender_name", "sender_email", "seller", "status", "created_at")
    list_filter = ("status", "is_spam", "created_at")
    search_fields = ("listing__title", "sender_name", "sender_email", "sender_phone")
    autocomplete_fields = ("listing", "seller", "sender")

