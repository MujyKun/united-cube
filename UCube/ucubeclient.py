import asyncio
from . import InvalidToken, LoginFailed
from . import BASE_SITE


class UCubeClient:
    """
    Abstract & Parent Client for connecting to UCube and creating the internal cache.

    .. warning:: Do not create an object directly from this class. Instead, create a :class:`UCube.UCubeClientSync` or :class:`UCube.UCubeClientAsync` object since those are concrete.

    Parameters
    ----------
    username: str
        Email or Username to log in with.
    password: str
        Password to log in with.
    verbose: bool
        Whether to print out verbose messages.
    web_session:
        An aiohttp or requests client session.
    token:
        The account token to connect to the UCube API.
        In order to find your token, please refer to :ref:`account_token`

    Attributes
    -----------
    verbose: bool
        Whether to print out verbose messages.
    web_session:
        An aiohttp or requests client session.
    user_notifications: list
        Most recent notifications of the account connected.
    cache_loaded: bool
        Whether the Internal UCache Cache is fully loaded.
        This will change for a split moment when grabbing a new post.
   """
    def __init__(self, username: str = None, password: str = None, token=None, web_session=None, verbose: bool = False):
        self.verbose = verbose
        self.web_session = web_session

        # we will allow invalid login information until the user uses the start method.
        self.__token = token

        self.__exception_to_raise = None

        self.user_notifications = []

        self._old_notifications = []
        self._headers: dict = self.__get_headers()

        self._base_site = BASE_SITE
        self._api_url = self._base_site + "v1/"

        # query string params that we will just append to the URL.
        self._club_slug = "?club={club_slug}"
        self._board_slug = "?board={board_slug}"
        self._per_page_and_number = "per_page={feed_amount}&page={page_number}"

        # slug is the unique identifier that UCube uses for a certain object.
        self._all_clubs_url = self._api_url + "clubs?" + self._per_page_and_number
        self._posts_url = self._api_url + "posts" + "?board={board_slug}&" + self._per_page_and_number
        self._boards_url = self._api_url + "boards" + self._club_slug
        self._feeds_url = self._api_url + "feeds" + self._board_slug + f"&{self._per_page_and_number}"
        self._notifications_url = self._api_url + "notifications" + self._club_slug + f"&{self._per_page_and_number}"

        self._club_info_url = self._api_url + "clubs/{club_slug}"
        # to this point, categories has not actually returned any items and is useless.
        self._categories_url = self._api_url + "boards/{club_slug}/categories"

        self._auth_login_url = self._api_url + "auth/login"
        self._sign_in_path_url = self._base_site + "signin"

        self._about_me_url = self._api_url + "me"

        self._login_payload = {
            "id": username,
            "path": self._sign_in_path_url,
            "pw": password,
            "refresh_token": None,
            "remember_me": True
        }

        self.__my_info = {
        }

        self.cache_loaded = False

        # Whether a UCube Client owns the web session or if it belongs to another application.
        self._own_session = False

        self.all_clubs = {}
        self.all_boards = {}

    @property
    def _login_info_exists(self) -> bool:
        """Whether login info is present."""
        return self._login_payload["id"] and self._login_payload["pw"]

    @property
    def _token_exists(self) -> bool:
        """Whether a token is present."""
        return bool(self.__token)

    async def _wait_for_login(self, timeout=15):
        """
        Will wait until the client is logged in or the timeout timer is exceed.

        Parameters
        ----------
        timeout: int
            Amount of seconds before an exception is raised.

        :raises:
        """
        seconds_passed = 0
        while not self._login_payload["refresh_token"]:
            if self.__exception_to_raise:
                if isinstance(self.__exception_to_raise, (LoginFailed, asyncio.exceptions.TimeoutError)):
                    exception = self.__exception_to_raise
                    self.__exception_to_raise = None
                    # if an exception was raised from here, the actual exception occurred in a task.
                    raise exception
            await asyncio.sleep(1)
            seconds_passed += 1

            if seconds_passed > timeout:
                self._set_exception(asyncio.exceptions.TimeoutError())

    @staticmethod
    def replace(url, **kwargs) -> str:
        """
        Will replace the args in an endpoint url.

        Parameters
        ----------
        url: str
            The URL to replace args for.
        kwargs: dict
            The args that need to be replaced followed by what they need to be replaced with.

        Returns
        -------
        str
        """
        for key, item in kwargs.items():
            url = url.replace(key, item)
        return url

    def _login(self, method):
        """
        Requests a login.

        Will not return response.
        The method should handle the response itself.

        Parameters
        ----------
        method:
            The async/sync method to call. Should be able to take in the login payload.
        """
        if not asyncio.iscoroutinefunction(method):
            method(self._login_payload)
        else:
            asyncio.create_task(method(self._login_payload))

    def _set_refresh_token(self, refresh_token: str):
        """
        Set the refresh token.

        Parameters
        ----------
        refresh_token: str
            The refresh token to pass when logging in.
        """
        self._login_payload["refresh_token"] = refresh_token

    def _set_token(self, token):
        """
        Set the token used for endpoints.

        Parameters
        ----------
        token: str
            New token used for endpoints
        """
        self.__token = token
        self._headers = self.__get_headers()  # update headers

    def _set_my_info(self, my_info: dict):
        """
        Will set the client's personal account information.

        Parameters
        ----------
        my_info: The data from the about me url.
        """
        self.__my_info = my_info

    def _set_exception(self, exception: Exception):
        """
        Set an exception from a task that occurred.

        Parameters
        ----------
        exception: The Exception that was raised.
        """
        self.__exception_to_raise = exception

    def _check_status(self, status, url) -> bool:
        """
        Confirm the status of a URL

        :param status: Status code of url connection
        :param url: Link that we connected to.
        :return: True if the connection was a success.
        :raises: :ref:`invalid_token_exc` if there was an invalid token.
        """
        if status == 200:
            return True
        elif status == 401:
            raise InvalidToken
        elif status == 404:
            if self.verbose:
                # raise error.PageNotFound
                print("WARNING (NOT CRITICAL): " + url + " was not found.")
        else:
            if self.verbose:
                print("WARNING (NOT CRITICAL): " + url + " Failed to load. [Status: " + str(status) + "]")

    def __get_headers(self):
        return {'Authorization': f"Bearer {self.__token}"}
