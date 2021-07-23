class InvalidToken(Exception):
    """An Exception Raised When an Invalid Token was Supplied."""
    def __init__(self):
        super(InvalidToken, self).__init__("An Invalid Bearer Token was Supplied to UCube.")


class InvalidCredentials(Exception):
    """An Exception raised when no valid credentials were supplied."""
    def __init__(self, msg: str):
        super(InvalidCredentials, self).__init__(msg)


class SomethingWentWrong(Exception):
    """An Exception raised when something went wrong."""
    def __init__(self, msg: str):
        super(SomethingWentWrong, self).__init__(msg)


class PageNotFound(Exception):
    r"""
    An Exception Raised When a link was not found.

    Parameters
    ----------
    url: :class:`str`
        The link that was not found.
    """
    def __init__(self, url):
        super(PageNotFound, self).__init__(url + "was an invalid link.")


class BeingRateLimited(Exception):
    """An Exception Raised When UCube Is Being Rate-Limited."""
    def __init__(self):
        super(BeingRateLimited, self).__init__("UCube is rate-limiting the requests.")
