from django.db.models import Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from apps.listings.models import Listing, ListingStatus


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_qs = (
            Listing.objects.active()
            .select_related("brand", "car_model", "city", "seller__profile")
            .prefetch_related("images")
        )
        context["featured_listings"] = active_qs.filter(featured=True)[:8]
        context["latest_listings"] = active_qs[:12]
        context["popular_cities"] = (
            Listing.objects.active()
            .values("city__name", "city__slug")
            .annotate(total=Count("id"))
            .order_by("-total", "city__name")[:8]
        )
        context["stats"] = {
            "active_count": Listing.objects.active().count(),
            "sold_count": Listing.objects.filter(status=ListingStatus.SOLD).count(),
        }
        return context


class ContactPageView(TemplateView):
    template_name = "core/contact.html"


def healthcheck(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)
