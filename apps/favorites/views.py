from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView

from apps.listings.models import Listing

from .models import Favorite
from .services import toggle_favorite


class FavoriteListView(LoginRequiredMixin, ListView):
    template_name = "favorites/favorite_list.html"
    context_object_name = "favorites"
    paginate_by = 12

    def get_queryset(self):
        return (
            Favorite.objects.filter(user=self.request.user)
            .select_related("listing", "listing__brand", "listing__car_model", "listing__city")
            .prefetch_related("listing__images")
        )


class FavoriteToggleView(LoginRequiredMixin, View):
    def post(self, request, slug):
        listing = get_object_or_404(Listing.objects.active(), slug=slug)
        is_favorite = toggle_favorite(request.user, listing)
        context = {"listing": listing, "is_favorite": is_favorite}
        template = "listings/partials/favorite_button.html"
        return render(request, template, context)

