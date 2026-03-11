from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from PIL import Image, UnidentifiedImageError

MAX_IMAGE_SIZE_BYTES = 8 * 1024 * 1024
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}


def validate_phone_number(value: str) -> None:
    cleaned = "".join(char for char in value if char.isdigit() or char == "+")
    if len(cleaned.replace("+", "")) < 8:
        raise ValidationError(_("Внесете валиден телефонски број."))


def validate_image_file(image) -> None:
    if image.size > MAX_IMAGE_SIZE_BYTES:
        raise ValidationError(_("Сликата мора да биде помала од 8MB."))

    try:
        image_bytes = image.read()
        opened = Image.open(BytesIO(image_bytes))
        opened.verify()
        if opened.format not in ALLOWED_IMAGE_FORMATS:
            raise ValidationError(_("Неподдржан формат на слика."))
    except (UnidentifiedImageError, OSError) as exc:
        raise ValidationError(_("Прикачете валидна слика.")) from exc
    finally:
        image.seek(0)


def normalize_uploaded_image(image):
    try:
        opened = Image.open(image)
        if opened.mode not in ("RGB", "L"):
            opened = opened.convert("RGB")
        buffer = BytesIO()
        opened.save(buffer, format="JPEG", quality=88, optimize=True)
        buffer.seek(0)
        return ContentFile(buffer.read(), name=f"{image.name.rsplit('.', 1)[0]}.jpg")
    except (UnidentifiedImageError, OSError):
        image.seek(0)
        return image
