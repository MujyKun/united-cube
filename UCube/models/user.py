from typing import Optional

from . import BaseModel


class User(BaseModel):
    r"""
    A User object that represents a UCube User.

    Inherits from :class:`BaseModel`

    .. warning::
        It is not suggested to create a User manually,
        but rather through the following method: :class:`UCube.objects.create_user`

    ``The information retrieved on a User is directly from the UCube API and altered to fit this class.``

    .. container:: operations

        .. describe:: x == y

            Checks if two Users have the same slug.

        .. describe:: x != y

            Checks if two Users do not have the same slug.

        .. describe:: str(x)

            Returns the User's name.

    Parameters
    ----------
    slug: :class:`str`
        The unique identifier of the User..
    nick_name: :class:`str`
        The name of the user.
    base_url: :class:`str`
        The Base URL of the image site.
        This is especially useful if there are several base urls for an image if UCube is using an external image host.
    profile_path: :class:`str`
        The path to the profile photo of the user.

    Attributes
    ----------
    profile_image: Optional[:class:`str`]
        The URL to the profile photo of the user.


    """
    def __init__(self, slug: str, base_url: str, **options):
        super().__init__(slug, options.get("nick_name") or options.get("artist_name"))
        image = options.pop("profile_path", None)

        self.profile_image = None if not image else base_url + image
