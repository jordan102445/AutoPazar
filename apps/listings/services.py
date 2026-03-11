from django.db import transaction
from django.utils import timezone

from apps.core.validators import normalize_uploaded_image

from .choices import ListingStatus
from .models import ListingImage


def _apply_submit_action(listing, submit_action):
    if submit_action == "publish":
        listing.status = ListingStatus.PENDING
    elif submit_action == "draft":
        listing.status = ListingStatus.DRAFT


@transaction.atomic
def save_listing_from_form(form, seller=None, image_formset=None, submit_action="draft"):
    listing = form.save(commit=False)
    if seller is not None and not listing.pk:
        listing.seller = seller
    _apply_submit_action(listing, submit_action)
    listing.save()

    if image_formset is not None:
        image_formset.instance = listing
        image_formset.save()

    uploaded_images = form.cleaned_data.get("new_images", [])
    for sort_order, uploaded in enumerate(uploaded_images, start=listing.images.count()):
        normalized = normalize_uploaded_image(uploaded)
        ListingImage.objects.create(
            listing=listing,
            image=normalized,
            sort_order=sort_order,
            is_cover=listing.images.count() == 0 and sort_order == 0,
        )

    _ensure_single_cover_image(listing)
    return listing


def _ensure_single_cover_image(listing):
    images = list(listing.images.order_by("sort_order", "id"))
    if not images:
        return

    cover_images = [image for image in images if image.is_cover]
    if not cover_images:
        first_image = images[0]
        first_image.is_cover = True
        first_image.save(update_fields=["is_cover"])
        return

    first_cover = cover_images[0]
    listing.images.exclude(pk=first_cover.pk).filter(is_cover=True).update(is_cover=False)


def change_listing_status(listing, action):
    if action == "mark_sold":
        listing.status = ListingStatus.SOLD
    elif action == "archive":
        listing.status = ListingStatus.ARCHIVED
    elif action == "reactivate":
        listing.status = ListingStatus.PENDING
    elif action == "publish":
        listing.status = ListingStatus.PENDING
    elif action == "draft":
        listing.status = ListingStatus.DRAFT
    elif action == "delete":
        listing.delete()
        return listing

    if listing.status == ListingStatus.ACTIVE and not listing.published_at:
        listing.published_at = timezone.now()
    listing.save(update_fields=["status", "updated_at", "published_at"])
    return listing


def increment_listing_views(listing, viewer=None):
    if viewer and viewer.is_authenticated and viewer == listing.seller:
        return
    listing.increment_views()
