from . import BaseModel
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .image import Image
    from .video import Video
    from .user import User
    from .comment import Comment


class Post(BaseModel):
    r"""
    A Post object that represents a UCube Post.

    Inherits from :class:`BaseModel`

    .. warning::
        It is not suggested to create a Post manually,
        but rather through the following method: :class:`UCube.objects.create_post`

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
        The unique identifier of the Post.
    create_image: :class:`UCube.create_image`
        The method to call for creating an image. You can also use a custom method.
    create_video: :class:`UCube.create_video`
        The method to call for creating a video. You can also use a custom method.
    create_user: :class:`UCube.create_user`
        The method to call for creating a user. You can also use a custom method.
    content: :class:`str`
        The body content of the post with HTML.
    board_slug: :class:`str`
        The board slug that the post belongs to.
    media: List[:class:`dict`]
        Media that belongs to a post.
    base_url: :class:`str`
        The Base URL of the image site. This is especially useful if there are several base urls for an image if
        UCube is using an external image host.

    Attributes
    ----------
    slug: :class:`str`
        The unique identifier of the Post.
    content: :class:`str`
        The post content (without HTML).
    board_slug: :class:`str`
        The Post Board slug.
    videos: List[:class:`Video`]
        A list of videos that belong to the post.
    images: List[:class:`Image`]
        A list of images that belong to the Post.
    comment_count: :class:`int`
        The amount of comments.
    posted_at: :class:`str`
        When the post was created.
    user: Optional[:class:`User`]
        The user that created the Post.
    comments: List[:class:`Comment`]
        A list of comments that belong to the Post.
    """
    def __init__(self, create_image, create_video, create_user, **options):
        super().__init__(options.get("slug"), options.get("name"))
        self.content: str = self.remove_html(options.pop("content", ""))

        self.board_slug: str = options.pop("board_slug", None)

        self.images: List[Image] = []
        self.videos: List[Video] = []

        media = options.pop("media", [])

        for media_obj in media:
            media_obj["data"]["base_url"] = options.get("base_url")
            if media_obj["type_code"] == "601":  # images
                self.images.append(create_image(media_obj["data"]))
            elif media_obj["type_code"] == "602":  # videos
                self.videos.append(create_video(media_obj["data"]))

        self.comment_count: int = options.pop("comment_count", None)
        self.posted_at = options.pop("register_datetime", None)
        user = options.pop("registrant", None)
        self.user: Optional[User] = None if not user else create_user(user)

        self.comments: List[Comment] = []

    def __str__(self):
        return self.content
