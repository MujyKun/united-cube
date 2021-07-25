import re
from typing import Optional


class BaseModel:
    r"""
    The Base Class for Model objects.

    .. container:: operations

        .. describe:: x == y

            Checks if two models have the same slug.

        .. describe:: x != y

            Checks if two models do not have the same slug.

        .. describe:: str(x)

            Returns the model's name.

    Parameters
    ----------
    slug: :class:`str`
        The unique identifier of the model.

    Other Parameters
    ----------------
    name: Optional[:class:`str`]
        The name of the object.

    Attributes
    ----------
    slug: :class:`str`
        The unique identifier.
    name: Optional[:class:`str`]
        The name of the object.
    """
    def __init__(self, slug: str, name: str = None):
        self.slug: str = slug
        self.name: Optional[str] = name

    def __eq__(self, other):
        return self.slug == other.slug

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return self.name

    @staticmethod
    def remove_html(content: str) -> str:
        """
        Removes HTML tags of the html content and returns a cleansed version.

        Parameters
        ----------
        content: :class:`str`
            The raw html content to remove html tags from.

        Returns
        -------
        A cleansed string with no HTML.: :class:`str`
        """
        if not content:
            return ""

        content = content.replace("<br>", "\n")  # replace new line tags before they get replaced.
        html_cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        clean_text = re.sub(html_cleaner, '', content)
        return clean_text
