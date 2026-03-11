from django.contrib import admin

from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "display_order", "is_active")
    list_filter = ("region", "is_active")
    search_fields = ("name", "region")
    prepopulated_fields = {"slug": ("name",)}

