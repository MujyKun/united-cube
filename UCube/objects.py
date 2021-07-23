from .models import Club, Image, Post, Video, Board

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


def create_board(raw_board: dict) -> Board:
    """

    Parameters
    ----------
    raw_board: dict
        The raw information about a board directly from a UCube API endpoint.

    Returns
    -------
    A Board Model: :class:`UCube.models.Board`
    """
    return Board(**raw_board)


def create_image(raw_image) -> Image:
    """

    Parameters
    ----------
    raw_image: dict
        The raw information about an image directly from a UCube API endpoint.

    Returns
    -------
    An Image Model: :class:`UCube.models.Image`

    """
    raw_image["base_url"] = BASE_SITE
    return Image(**raw_image)


def create_video(raw_video) -> Video:
    """

    Parameters
    ----------
    raw_video: dict
        The raw information about a video directly from a UCube API endpoint.

    Returns
    -------
    A Video Model: :class:`UCube.models.Video`

    """
    return Video(**raw_video)


def create_post(raw_post) -> Post:
    """

    Parameters
    ----------
    raw_post: dict
        The raw information about a post directly from a UCube API endpoint.

    Returns
    -------
    A Post Model: :class:`UCube.models.Post`
    """
    raw_post["create_image"] = create_image
    raw_post["create_video"] = create_video
    raw_post["base_url"] = BASE_SITE
    return Post(**raw_post)

