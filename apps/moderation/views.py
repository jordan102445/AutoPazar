from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit

from apps.listings.models import Listing

from .forms import ListingReportForm
from .services import create_listing_report


@method_decorator(ratelimit(key="ip", rate=settings.REPORT_RATE, method="POST", block=True), name="dispatch")
class ListingReportCreateView(View):
    def post(self, request, slug):
        listing = get_object_or_404(Listing.objects.active(), slug=slug)
        form = ListingReportForm(request.POST)
        if form.is_valid():
            create_listing_report(listing, form, request)
            messages.success(request, "Пријавата е успешно испратена.")
            if getattr(request, "htmx", False):
                return render(request, "moderation/report_success.html", {"listing": listing})
        else:
            messages.error(request, "Пријавата не можеше да се испрати.")
        return redirect("listings:detail", slug=listing.slug)
