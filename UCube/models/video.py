from typing import Optional

from . import BaseModel


class Video(BaseModel):
    r"""
    A Video object that represents a UCube Video.

    Inherits from :class:`BaseModel`

    .. warning::
        It is not suggested to create a Video manually,
        but rather through the following method: :class:`UCube.objects.create_video`

    ``The information retrieved on a Video is directly from the UCube API and altered to fit this class.``

    .. container:: operations

        .. describe:: x == y

            Checks if two Videos have the same url (slug for a video).

        .. describe:: x != y

            Checks if two Videos have the same url (slug for a video).

        .. describe:: str(x)

            Returns the Video's slug (url).

    Parameters
    ----------
    slug: :class:`str`
        The unique identifier of the video. This can be the full link to the video.
    url: :class:`str`
        The URL of the video.
    name: :class:`str`
        The title of the video. This can also be passed in as title.
    image: :class:`str`
        The link to the thumbnail.

    Attributes
    ----------
    slug: :class:`str`
        The unique identifier of the video. This can be the full link to the video.
    name: :class:`str`
        The title of the video.
    url: :class:`str`
        The URL to the Video.
    thumbnail: :class:`str`
        The thumbnail of the video.
    """
    def __init__(self, url, **options):
        if not options.get("slug"):
            # The slug will become the url if it does not exist.
            options["slug"] = url
        if options.get("title") and not options.get("name"):
            options["name"] = options["title"]
        super().__init__(options.get("slug"), options.get("name"))

        self.url: str = url
        self.thumbnail: Optional[str] = options.pop("image", None)
