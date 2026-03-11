from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.TextChoices):
    EUR = "EUR", _("EUR")
    MKD = "MKD", _("MKD")


class FuelType(models.TextChoices):
    PETROL = "petrol", _("Бензин")
    DIESEL = "diesel", _("Дизел")
    LPG = "lpg", _("LPG")
    CNG = "cng", _("CNG")
    HYBRID = "hybrid", _("Хибрид")
    ELECTRIC = "electric", _("Електричен")


class TransmissionType(models.TextChoices):
    MANUAL = "manual", _("Мануелен")
    AUTOMATIC = "automatic", _("Автоматски")
    SEMI_AUTOMATIC = "semi_automatic", _("Полуавтоматски")


class BodyType(models.TextChoices):
    SEDAN = "sedan", _("Седан")
    HATCHBACK = "hatchback", _("Хечбек")
    COUPE = "coupe", _("Купе")
    CABRIO = "cabrio", _("Кабриолет")
    WAGON = "wagon", _("Караван")
    SUV = "suv", _("SUV")
    PICKUP = "pickup", _("Пикап")
    VAN = "van", _("Комбе")


class DriveType(models.TextChoices):
    FWD = "fwd", _("Преден погон")
    RWD = "rwd", _("Заден погон")
    AWD = "awd", _("Погон на сите тркала")
    FOUR_X_FOUR = "4x4", _("4x4")


class ListingCondition(models.TextChoices):
    USED = "used", _("Користен")
    NEW = "new", _("Нов")
    DAMAGED = "damaged", _("Оштетен")


class ListingStatus(models.TextChoices):
    DRAFT = "draft", _("Нацрт")
    PENDING = "pending_moderation", _("Чека одобрување")
    ACTIVE = "active", _("Активен")
    SOLD = "sold", _("Продаден")
    ARCHIVED = "archived", _("Архивиран")
