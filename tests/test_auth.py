import pytest
from django.urls import reverse

from tests.factories import CityFactory

pytestmark = pytest.mark.django_db


def test_user_can_register_and_login(client, password):
    city = CityFactory(name="Skopje")
    response = client.post(
        reverse("users:register"),
        data={
            "email": "new@example.com",
            "full_name": "Nov Korisnik",
            "phone_number": "+38970111222",
            "city": city.pk,
            "password1": password,
            "password2": password,
        },
        follow=True,
    )

    assert response.status_code == 200
    assert response.wsgi_request.user.is_authenticated

    client.logout()
    login_response = client.post(
        reverse("users:login"),
        data={"username": "new@example.com", "password": password},
        follow=True,
    )
    assert login_response.status_code == 200
    assert login_response.wsgi_request.user.is_authenticated


def test_profile_page_requires_authentication(client):
    response = client.get(reverse("users:profile"))
    assert response.status_code == 302
    assert reverse("users:login") in response.headers["Location"]
