from . import BaseModel


class Notification(BaseModel):
    r"""
    A Notification object that represents a UCube Notification.

    Inherits from :class:`BaseModel`

    .. warning::
        It is not suggested to create a Notification manually, but rather through the following method:
        :class:`UCube.objects.create_notification`

    ``The information retrieved on a Notification is directly from the UCube API and altered to fit this class.``

    .. container:: operations

        .. describe:: x == y

            Checks if two Notifications have the same slug.

        .. describe:: x != y

            Checks if two Notifications do not have the same slug.

        .. describe:: str(x)

            Returns the Notification's title.

    Parameters
    ----------
    uid: :class:`str`
        The unique identifier (basically a Slug) of the Notification.

    Attributes
    ----------
    body: :class:`str`
        The content of the notification.
    topic_slug: :class:`str`
        The slug of the topic.
    channel_type: :class:`str`
        The channel type of the Notification.
    created_at: :class:`str`
        The timestamp of when the Notification was created.
    direct_link: :class:`str`
        Direct link to access the content.
    data_type: :class:`str`
        The type of the data.
    club_name: :class:`str`
        The club's name.
    club_slug: :class:`str`
        The club's slug.
    post_slug: :class:`str`
        The slug of the Post.
    board_name: :class:`str`
        The name of the Board.
    board_slug: :class:`str`
        The slug (unique identifier) of the board.
    board_type: :class:`str`
        The type of the Board.


    """
    def __init__(self, uid, **options):
        super().__init__(str(uid), options.get("title"))
        self.body: str = options.pop("body", None)
        self.topic_slug: str = options.pop("topic", None)
        self.channel_type: str = options.pop("channel", None)  # usually "notification"
        self.created_at: str = options.pop("register_datetime", None)
        data = options.get("data") or {}
        self.direct_link = data.pop("link", None)
        self.data_type = data.pop("type", None)  # usually "notification"
        self.club_name = data.pop("club_name", None)
        self.club_slug = data.pop("club_slug", None)
        self.post_slug = data.pop("post_slug", None)
        self.board_name = data.pop("board_name", None)
        self.board_slug = data.pop("board_slug", None)
        self.board_type = data.pop("board_type", None)
