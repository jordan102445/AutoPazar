from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views import View
from django.views.generic import DetailView, FormView, TemplateView, UpdateView
from django_ratelimit.decorators import ratelimit

from apps.listings.models import Listing, ListingStatus
from apps.messaging.models import InquiryMessage, InquiryStatus

from .forms import EmailAuthenticationForm, UserProfileForm, UserRegistrationForm
from .services import send_verification_email

User = get_user_model()


@method_decorator(ratelimit(key="ip", rate=settings.REGISTER_RATE, method="POST", block=True), name="dispatch")
@method_decorator(never_cache, name="dispatch")
class RegisterView(FormView):
    template_name = "users/auth/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:dashboard")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_verification_email(user, self.request)
        messages.success(self.request, "Профилот е успешно креиран.")
        return super().form_valid(form)


@method_decorator(ratelimit(key="ip", rate=settings.LOGIN_RATE, method="POST", block=True), name="dispatch")
@method_decorator(never_cache, name="dispatch")
class EmailLoginView(LoginView):
    template_name = "users/auth/login.html"
    authentication_form = EmailAuthenticationForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "users/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        listings = (
            Listing.objects.visible_for_owner(user)
            .select_related("brand", "car_model", "city")
            .prefetch_related("images")
        )
        context["stats"] = {
            "active": listings.filter(status=ListingStatus.ACTIVE).count(),
            "pending": listings.filter(status=ListingStatus.PENDING).count(),
            "favorites": user.favorites.count(),
            "inquiries": InquiryMessage.objects.filter(seller=user, status=InquiryStatus.NEW).count(),
        }
        context["recent_listings"] = listings[:6]
        context["recent_inquiries"] = (
            InquiryMessage.objects.filter(seller=user)
            .select_related("listing", "sender")
            .order_by("-created_at")[:6]
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, "Профилот е успешно ажуриран.")
        return super().form_valid(form)


class EmailVerificationSentView(LoginRequiredMixin, TemplateView):
    template_name = "users/email_verification_sent.html"


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError) as exc:
            raise Http404 from exc

        if default_token_generator.check_token(user, token):
            user.email_verified_at = timezone.now()
            user.save(update_fields=["email_verified_at"])
            messages.success(request, "Е-поштата е успешно потврдена.")
            return redirect("users:login")

        messages.error(request, "Линкот за потврда не е валиден.")
        return redirect("users:login")


class PublicSellerProfileView(DetailView):
    model = User
    template_name = "users/public_profile.html"
    context_object_name = "seller"

    def get_queryset(self):
        return User.objects.select_related("profile", "profile__city")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_listings"] = (
            Listing.objects.active()
            .filter(seller=self.object)
            .select_related("brand", "car_model", "city")
            .prefetch_related("images")
        )
        return context
