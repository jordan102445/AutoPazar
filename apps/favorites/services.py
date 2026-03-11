from .models import Favorite


def toggle_favorite(user, listing):
    favorite, created = Favorite.objects.get_or_create(user=user, listing=listing)
    if not created:
        favorite.delete()
        return False
    return True

