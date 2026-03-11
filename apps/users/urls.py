from django.contrib.auth.views import (
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path, reverse_lazy

from .views import (
    DashboardView,
    EmailLoginView,
    EmailVerificationSentView,
    ProfileUpdateView,
    PublicSellerProfileView,
    RegisterView,
    VerifyEmailView,
)

app_name = "users"

urlpatterns = [
    path("najava/", EmailLoginView.as_view(), name="login"),
    path("odjava/", LogoutView.as_view(), name="logout"),
    path("registracija/", RegisterView.as_view(), name="register"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("profil/", ProfileUpdateView.as_view(), name="profile"),
    path("email/ispraateno/", EmailVerificationSentView.as_view(), name="email-verification-sent"),
    path("email/potvrda/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify-email"),
    path(
        "lozinka/reset/",
        PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="emails/password_reset_email.txt",
            success_url=reverse_lazy("users:password-reset-done"),
        ),
        name="password-reset",
    ),
    path(
        "lozinka/reset/ispraateno/",
        PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name="password-reset-done",
    ),
    path(
        "lozinka/reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("users:password-reset-complete"),
        ),
        name="password-reset-confirm",
    ),
    path(
        "lozinka/reset/gotovo/",
        PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name="password-reset-complete",
    ),
    path("prodavac/<int:pk>/", PublicSellerProfileView.as_view(), name="public-profile"),
]
