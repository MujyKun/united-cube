from . import BaseModel
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .image import Image
    from .video import Video


class Post(BaseModel):
    r"""
    A Post object that represents a UCube Post.

    Inherits from :class:`BaseModel`

    .. warning:: It is not suggested to create a Post manually, but rather through the following method: :class:`UCube.objects.create_post`

    ``The information retrieved on a Post is directly from the UCube API and altered to fit this class.``

    .. container:: operations

        .. describe:: x == y

            Checks if two Posts have the same slug.

        .. describe:: x != y

            Checks if two Posts have the same slug.

        .. describe:: str(x)

            Returns the Post's content.

    Parameters
    ----------
    slug: :class:`str`
        The unique identifier of the image. This can be the full link to the image.
    create_image: :class:`UCube.create_image`
        The method to call for creating an image.
    create_video: :class:`UCube.create_video`
        The method to call for creating a video.
    content: :class:`str`
        The body content of the post with HTML.
    board_slug: :class:`str`
        The board slug that the post belongs to.
    media: List[:class:`dict`]
        Media that belongs to a post.
    base_url: :class:`str`
        The Base URL of the image site. This is especially useful if there are several base urls for an image if UCube is using an external image host.

    Attributes
    ----------
    slug: :class:`str`
        The unique identifier of the image. This can be the full link to the image.
    content: :class:`str`
        The post content (without HTML).
    path: :class:`str`
        The path to the direct link of the image.
    size: :class:`int`
        The size of the Image.
    width: :class:`int`
        The width of the Image. This may be set to 0 at times.
    height: :class:`int`
        The height of the Image. This may be set to 0 at times.
    """
    def __init__(self, create_image, create_video, **options):
        super().__init__(options.get("slug"), options.get("name"))
        self.content: str = self.remove_html(options.pop("content", ""))

        self.images: List[Image] = []
        self.videos: List[Video] = []

        media = options.pop("media", [])

        for media_obj in media:
            media_obj["data"]["base_url"] = options.get("base_url")
            if media_obj["type_code"] == "601":  # images
                self.images.append(create_image(media_obj["data"]))
            elif media_obj["type_code"] == "602":  # videos
                self.videos.append(create_video(media_obj["data"]))

    def __str__(self):
        return self.content
