from django.contrib import admin

from .choices import ListingStatus
from .models import CarBrand, CarModel, Listing, ListingImage


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 0


@admin.action(description="Одобри ги избраните огласи")
def approve_listings(modeladmin, request, queryset):
    queryset.update(status=ListingStatus.ACTIVE)


@admin.action(description="Испрати ги избраните огласи на модерација")
def pend_listings(modeladmin, request, queryset):
    queryset.update(status=ListingStatus.PENDING)


@admin.action(description="Означи ги избраните огласи како продадени")
def mark_sold(modeladmin, request, queryset):
    queryset.update(status=ListingStatus.SOLD)


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "is_active")
    list_filter = ("brand", "is_active")
    search_fields = ("name", "brand__name")


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "brand", "car_model", "city", "price", "status", "featured", "created_at")
    list_filter = ("status", "featured", "city", "brand", "fuel_type", "transmission", "body_type")
    search_fields = ("title", "description", "seller__email", "seller__profile__full_name", "vin")
    autocomplete_fields = ("seller", "brand", "car_model", "city")
    inlines = [ListingImageInline]
    actions = [approve_listings, pend_listings, mark_sold]
    readonly_fields = ("view_count", "created_at", "updated_at", "deleted_at")
    list_select_related = ("seller", "brand", "car_model", "city")


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ("listing", "sort_order", "is_cover", "created_at")
    list_filter = ("is_cover",)
    autocomplete_fields = ("listing",)
