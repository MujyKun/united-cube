from .models import Club, Image

BASE_SITE = "https://united-cube.com/"


def create_club(raw_club: dict) -> Club:
    """

    Parameters
    ----------
    raw_club: dict
        The raw information about a club directly from a UCube API endpoint.

    Returns
    -------
    A Club Model: :class:`UCube.models.Club`
    """
    raw_club["create_image"] = create_image
    return Club(**raw_club)


def create_image(raw_image) -> Image:
    """

    Parameters
    ----------
    raw_image: dict
        The raw information about a club directly from a UCube API endpoint.

    Returns
    -------
    An Image Model: :class:`UCube.models.Image`

    """
    raw_image["base_api_url"] = BASE_SITE
    return Image(**raw_image)
