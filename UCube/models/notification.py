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

            Returns the Notification's content.

    Parameters
    ----------
    slug: :class:`str`
        The unique identifier of the User..

    Attributes
    ----------


    """
    def __init__(self, slug: str, **options):
        super().__init__(slug)


