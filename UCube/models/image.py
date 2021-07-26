from . import BaseModel


class Image(BaseModel):
    r"""
    An Image object that represents a UCube Image/Logo.

    Inherits from :class:`BaseModel`

    .. warning:: It is not suggested to create an Image manually, but rather through the following method:
        :class:`UCube.objects.create_image`

    ``The information retrieved on an Image is directly from the UCube API and altered to fit this class.``

    .. container:: operations

        .. describe:: x == y

            Checks if two Images have the same path.

        .. describe:: x != y

            Checks if two Images have the same path.

        .. describe:: str(x)

            Returns the Image's name.

        .. describe:: int(x)

            Returns the Image's size.

    Parameters
    ----------
    slug: :class:`str`
        The unique identifier of the image. This can be the full link to the image.
    path: :class:`str`
        The path to the direct link of the image.
    base_url: :class:`str`
        The Base URL of the image site.
        This is especially useful if there are several base urls for an image if UCube is using an external image host.

    Other Parameters
    ----------------
    size: :class:`int`
        The size of the Image. This may be set to 0 if it is unknown.
    width: :class:`int`
        The width of the Image. This may be set to 0 if it is unknown.
    height: :class:`int`
        The height of the Image. This may be set to 0 if it is unknown.

    Attributes
    ----------
    slug: :class:`str`
        The unique identifier of the image. This can be the full link to the image.
    base_url: :class:`str`
        The Base URL of the image site.
    path: :class:`str`
        The path to the direct link of the image.
    size: :class:`int`
        The size of the Image.
    width: :class:`int`
        The width of the Image. This may be set to 0 at times.
    height: :class:`int`
        The height of the Image. This may be set to 0 at times.
    """
    def __init__(self, path, base_url, **options):
        if "https://" not in path:
            path = base_url + path
        if not options.get("slug"):
            # The slug will become the path if it does not exist.
            options["slug"] = path
        super().__init__(options.get("slug"), self.__extract_photo_name(path))

        self.path: str = path
        self.size: int = options.pop("size", 0)
        self.width: int = options.pop("width", 0)
        self.height: int = options.pop("height", 0)

    def __int__(self):
        return self.size

    def __extract_photo_name(self, url: str):
        """Retrieve the file name of the photo from the url.

        :param url: :class:`str`
            The URL of the photo.
        """
        last_slash_pos = url.rfind("/")
        if last_slash_pos == -1:
            return None
        elif last_slash_pos == len(url) - 1:
            return self.__extract_photo_name(url[0:len(url) - 1])
        else:
            return url[last_slash_pos + 1: len(url)]
