from . import BaseModel


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
    slug: :class:`str`
        The unique identifier of the User..

    Attributes
    ----------


    """
    def __init__(self, slug: str, **options):
        super().__init__(slug)


