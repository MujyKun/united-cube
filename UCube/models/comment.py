from . import BaseModel
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from . import User


class Comment(BaseModel):
    r"""
    A Comment object that represents a UCube Comment.

    Inherits from :class:`BaseModel`

    .. warning::
        It is not suggested to create a Comment manually, but rather through the following method:
        :class:`UCube.objects.create_comment`

    ``The information retrieved on a Comment is directly from the UCube API and altered to fit this class.``

    .. container:: operations

        .. describe:: x == y

            Checks if two Comments have the same slug.

        .. describe:: x != y

            Checks if two Comments do not have the same slug.

        .. describe:: str(x)

            Returns the Comment's content.

    Parameters
    ----------
    uid:
        The unique identifier (basically a Slug) of the Comment.
    create_user: :class:`UCube.create_user`
        The method to call for creating a user. You can also use a custom method.

    Attributes
    ----------
    comment_count: :class:`int`
        Amount of comments that belong to the comment.
    content: :class:`str`
        Content of the comment
    parent_slug: :class:`str`
        The parent slug/uid if there was one.
    created_at: :class:`str`
        The timestamp for when the comment was created.
    user: Optional[:class:`User`]
        The User that created the comment.
    """
    def __init__(self, uid, create_user, **options):
        super().__init__(str(uid))
        self.comment_count: int = options.pop("comment_count", None)
        self.content: str = options.pop("content", None)
        parent_slug = options.get("parent_uid")
        self.parent_slug: str = None if not parent_slug else str(parent_slug)
        self.created_at: str = options.pop("register_datetime", None)
        user = options.pop("registrant", None)
        self.user: Optional[User] = None if not user else create_user(user)

    def __str__(self):
        return self.content
