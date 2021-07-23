from .models import Club, Image

BASE_SITE = "https://united-cube.com/"


def create_club(raw_club: dict) -> Club:
    """lol"""
    raw_club["create_image"] = create_image
    return Club(**raw_club)


def create_image(raw_image) -> Image:
    """lol"""
    raw_image["base_api_url"] = BASE_SITE
    return Image(**raw_image)
