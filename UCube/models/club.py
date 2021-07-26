from typing import Optional, TYPE_CHECKING, Dict, List

from . import BaseModel

if TYPE_CHECKING:
    from .image import Image
    from .board import Board
    from .notification import Notification


class Club(BaseModel):
    r"""
    A Club object that represents a UCube Club.

    Inherits from :class:`BaseModel`

    .. warning::
        It is not suggested to create a Club manually,
        but rather through the following method: :class:`UCube.objects.create_club`

    ``The information retrieved on a Club is directly from the UCube API and altered to fit this class.``

    .. container:: operations

        .. describe:: x == y

            Checks if two Clubs have the same slug.

        .. describe:: x != y

            Checks if two Clubs do not have the same slug.

        .. describe:: str(x)

            Returns the Club's name.

    Parameters
    ----------
    slug: :class:`str`
        The unique identifier of the Club.
    artist_name: :class:`str`
        The artist's name. Could also be a group.
    create_image: :class:`UCube.create_image`
        The method to call for creating an image.

    Other Parameters
    ----------------
    color_1: :class:`str`
        The first color hex code.
    color_2: :class:`str`
        The second color hex code.
    artist_logo_file: :class:`dict`
        The raw information about the artist logo image.
    thumbnail_file: :class:`dict`
        The raw information about the thumbnail.
    thumbnail_small_file: :class:`dict`
        The raw information about the smaller version of the thumbnail.
    external_url: :class:`str`
        Any external url to the Club.
    register_datetime: :class:`str`
        The datetime for when the club was first registered.

    Attributes
    ----------
    artist_name: :class:`str`
        The artist's name. Could also be a group.
    artist_logo: Optional[:class:`Image`]
        The artist logo as an Image. May be None.
    color_one: :class:`str`
        The first color hex code.
    color_two: :class:`str`
        The second color hex code.
    thumbnail_image: Optional[:class:`Image`]
        The thumbnail Image for the Club.
    small_thumbnail_image: Optional[:class:`Image`]
        The smaller version of the thumbnail Image for the Club.
    external_url: :class:`str`
        Any external url to the Club.
    registered_time: :class:`str`
        The datetime for when the club was first registered.
    boards: Dict[:class:`str`, :class:`Board`]
        A Dict of Boards that belong to the Club with the slug as the key.
    notifications: List[:class:`Notification`]
        A list of Notifications that belong to the Club.

    """
    def __init__(self, artist_name: str, create_image, **options):
        super().__init__(options.get("slug"), artist_name)
        self.artist_name: str = artist_name
        self.color_one: Optional[str] = options.pop("color_1", None)
        self.color_two: Optional[str] = options.pop("color_2", None)

        artist_logo = options.get("artist_logo_file")
        self.artist_logo: Optional[Image] = None if not artist_logo else create_image(artist_logo)

        thumbnail_image = options.get("thumbnail_file")
        self.thumbnail: Optional[Image] = None if not thumbnail_image else create_image(thumbnail_image)

        small_thumbnail_image = options.get("thumbnail_small_file")
        self.small_thumbnail: Optional[Image] = None if not small_thumbnail_image else \
            create_image(small_thumbnail_image)

        self.external_url: str = options.pop("external_url", None)
        self.registered_time: str = options.pop("register_datetime", None)

        self.boards: Dict[str, Board] = {}
        self.notifications: List[Notification] = []
