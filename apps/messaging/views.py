from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from django_ratelimit.decorators import ratelimit

from apps.listings.models import Listing

from .forms import InquiryForm
from .models import InquiryMessage, InquiryStatus
from .services import create_inquiry


@method_decorator(ratelimit(key="ip", rate=settings.MESSAGE_RATE, method="POST", block=True), name="dispatch")
class InquiryCreateView(View):
    def post(self, request, slug):
        listing = get_object_or_404(Listing.objects.active(), slug=slug)
        form = InquiryForm(request.POST)
        if form.is_valid():
            try:
                create_inquiry(listing, form, request)
            except ValueError:
                messages.error(request, "Не можете да испратите порака за сопствен оглас.")
            else:
                messages.success(request, "Пораката е успешно испратена.")
                if getattr(request, "htmx", False):
                    return render(request, "messaging/inquiry_success.html", {"listing": listing})
                return redirect("listings:detail", slug=listing.slug)

        if getattr(request, "htmx", False):
            return render(
                request,
                "listings/partials/inquiry_form.html",
                {"listing": listing, "inquiry_form": form},
                status=400,
            )
        messages.error(request, "Проверете ги внесените податоци и обидете се повторно.")
        return redirect("listings:detail", slug=listing.slug)


class InboxListView(LoginRequiredMixin, ListView):
    template_name = "messaging/inbox.html"
    context_object_name = "messages"
    paginate_by = 20

    def get_queryset(self):
        return (
            InquiryMessage.objects.filter(seller=self.request.user)
            .select_related("listing", "sender")
            .order_by("-created_at")
        )


class InquiryStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        inquiry = get_object_or_404(InquiryMessage, pk=pk, seller=request.user)
        action = request.POST.get("action")
        if action == "archive":
            inquiry.status = InquiryStatus.ARCHIVED
        elif action == "reply":
            inquiry.status = InquiryStatus.REPLIED
        inquiry.save(update_fields=["status", "updated_at"])
        return redirect("messaging:inbox")
