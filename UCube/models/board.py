from typing import Dict, TYPE_CHECKING


from . import BaseModel

if TYPE_CHECKING:
    from .post import Post


class Board(BaseModel):
    r"""
    A Board object that represents a UCube Board.

    Inherits from :class:`BaseModel`

    .. warning::
        It is not suggested to create a Board manually,
        but rather through the following method: :class:`UCube.objects.create_board`

    ``The information retrieved on a Board is directly from the UCube API and altered to fit this class.``

    .. container:: operations

        .. describe:: x == y

            Checks if two Boards have the same slug.

        .. describe:: x != y

            Checks if two Boards do not have the same slug.

        .. describe:: str(x)

            Returns the Board's name.

    Parameters
    ----------
    slug: :class:`str`
        The unique identifier of the Board.
    active_flag: :class:`bool`
        Whether the board is active.
    club_slug: :class:`str`
        The club slug that the board belongs to.

    Attributes
    ----------
    active_flag: :class:`bool`
        Whether the board is active.
    club_slug: :class:`str`
        The club slug that the board belongs to.
    posts: Dict[:class:`str`, :class:`Post`]

    """
    def __init__(self, **options):
        super().__init__(options.get("slug"), options.get("name"))
        self.active_flag: bool = options.get("active_flag")
        self.club_slug: str = options.get("club_slug")
        self.posts: Dict[str, Post] = {}
