from django.contrib import admin

from .models import AuditLog, ListingReport


@admin.register(ListingReport)
class ListingReportAdmin(admin.ModelAdmin):
    list_display = ("listing", "reason", "status", "reporter", "created_at", "reviewed_at")
    list_filter = ("status", "reason", "created_at")
    search_fields = ("listing__title", "description", "reporter__email")
    autocomplete_fields = ("listing", "reporter", "reviewed_by")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("event_type", "actor", "listing", "ip_address", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("event_type", "actor__email", "listing__title")
    autocomplete_fields = ("actor", "listing")

