from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django_ratelimit.decorators import ratelimit

from apps.favorites.models import Favorite
from apps.messaging.forms import InquiryForm
from apps.moderation.forms import ListingReportForm

from .forms import ListingFilterForm, ListingForm, ListingImageFormSet
from .models import CarModel, Listing
from .selectors import filter_listings, listing_detail_queryset, owner_listing_queryset
from .services import change_listing_status, increment_listing_views, save_listing_from_form


class ListingListView(ListView):
    template_name = "listings/listing_list.html"
    context_object_name = "listings"
    paginate_by = 12

    def get_filter_form(self):
        return ListingFilterForm(self.request.GET or None)

    def get_queryset(self):
        self.filter_form = self.get_filter_form()
        if self.filter_form.is_valid():
            return filter_listings(self.filter_form.cleaned_data)
        return filter_listings({})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        return context

    def render_to_response(self, context, **response_kwargs):
        if getattr(self.request, "htmx", False):
            return render(self.request, "listings/partials/search_results.html", context)
        return super().render_to_response(context, **response_kwargs)


class ListingDetailView(DetailView):
    template_name = "listings/listing_detail.html"
    context_object_name = "listing"

    def get_queryset(self):
        return listing_detail_queryset(self.request.user)

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        obj = get_object_or_404(queryset, slug=self.kwargs["slug"])
        increment_listing_views(obj, self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listing = self.object
        context["inquiry_form"] = InquiryForm(
            initial=self._initial_inquiry_data(),
        )
        context["report_form"] = ListingReportForm()
        context["seller_other_listings"] = (
            listing.seller.listings.active()
            .exclude(pk=listing.pk)
            .select_related("brand", "car_model", "city")
            .prefetch_related("images")[:4]
        )
        context["is_favorite"] = False
        if self.request.user.is_authenticated:
            context["is_favorite"] = Favorite.objects.filter(
                user=self.request.user,
                listing=listing,
            ).exists()
        return context

    def _initial_inquiry_data(self):
        if not self.request.user.is_authenticated:
            return {}
        profile = self.request.user.profile
        return {
            "sender_name": profile.full_name,
            "sender_email": self.request.user.email,
            "sender_phone": profile.phone_number,
        }


@method_decorator(ratelimit(key="ip", rate=settings.LISTING_CREATE_RATE, method="POST", block=True), name="dispatch")
@method_decorator(never_cache, name="dispatch")
class ListingCreateView(LoginRequiredMixin, CreateView):
    template_name = "listings/listing_form.html"
    form_class = ListingForm

    def form_valid(self, form):
        self.object = save_listing_from_form(
            form,
            seller=self.request.user,
            submit_action=self.request.POST.get("submit_action", "draft"),
        )
        messages.success(self.request, "Огласот е успешно зачуван.")
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Нов оглас"
        context["image_formset"] = None
        return context

    def get_success_url(self):
        return reverse("listings:update", kwargs={"slug": self.object.slug})


@method_decorator(ratelimit(key="ip", rate=settings.LISTING_CREATE_RATE, method="POST", block=True), name="dispatch")
@method_decorator(never_cache, name="dispatch")
class ListingUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "listings/listing_form.html"
    form_class = ListingForm
    model = Listing
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return owner_listing_queryset(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = ListingImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
            )
        else:
            context["image_formset"] = ListingImageFormSet(instance=self.object)
        context["page_title"] = "Измени оглас"
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        image_formset = context["image_formset"]
        if not image_formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form))

        self.object = save_listing_from_form(
            form,
            image_formset=image_formset,
            submit_action=self.request.POST.get("submit_action", "draft"),
        )
        messages.success(self.request, "Промените се успешно зачувани.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("listings:update", kwargs={"slug": self.object.slug})


class ListingStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        listing = get_object_or_404(owner_listing_queryset(request.user), slug=slug)
        action = request.POST.get("action")
        if action not in {"publish", "draft", "mark_sold", "archive", "reactivate", "delete"}:
            raise Http404
        change_listing_status(listing, action)
        messages.success(request, "Статусот е успешно променет.")
        return redirect("users:dashboard")


class BrandModelOptionsView(View):
    def get(self, request):
        brand_id = request.GET.get("brand")
        models_qs = CarModel.objects.none()
        if brand_id:
            models_qs = CarModel.objects.filter(brand_id=brand_id, is_active=True)
        return render(request, "listings/partials/model_options.html", {"models": models_qs})
