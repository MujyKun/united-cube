from . import InvalidToken, SomethingWentWrong


class UCubeClient:
    """
    Abstract & Parent Client for connecting to UCube and creating the internal cache.

    Do not create an object directly from this class.
    Instead, create a :class:`UCube.UCubeClientSync` or :class:`UCube.UCubeClientAsync`
    object since those are concrete.

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

        self.user_notifications = []

        self._old_notifications = []
        self._headers: dict = self.__get_headers()

        self._base_site = "https://united-cube.com/"
        self._api_url = self._base_site + "v1/"

        # query string params that we will just append to the URL.
        self._club_slug = "?club={club_slug}"
        self._board_slug = "?board={board_slug}"
        self._per_page_and_number = "&per_page={feed_amount}&page={page_number}"

        # slug is the unique identifier that UCube uses for a certain object.
        self._boards_url = self._api_url + "boards" + self._club_slug
        self._feeds_url = self._api_url + "feeds" + self._board_slug + self._per_page_and_number
        self._notifications_url = self._api_url + "notifications" + self._club_slug + self._per_page_and_number

        self._club_info_url = self._api_url + "clubs/{club_slug}"
        # to this point, categories has not actually returned any items and is useless.
        self._categories_url = self._api_url + "boards/{club_slug}/categories"

        self._auth_login_url = self._api_url + "/auth/login"
        self._sign_in_path_url = self._base_site + "signin"

        self._about_me_url = self._api_url + "me"

        self.__login_payload = {
            "id": username,
            "path": self._sign_in_path_url,
            "pw": password,
            "refresh_token": None,
            "remember_me": True
        }

        self.__my_info = {
        }

        self.cache_loaded = False

        self.all_clubs = {}
        self.all_boards = {}

    @property
    def _login_info_exists(self) -> bool:
        """Whether login info is present."""
        return self.__login_payload["id"] and self.__login_payload["pw"]

    @property
    def _token_exists(self) -> bool:
        """Whether a token is present."""
        return bool(self.__token)

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

    def _login(self, method, async_method=False, loop=None):
        """
        Requests a login.

        Will not return response.
        The method should handle the response itself.

        Parameters
        ----------
        method:
            The method to call. Should be able to take in the login payload.
        async_method: bool
            Whether or not the method to call is asynchronous
        loop:
            Asyncio Event Loop. This should be passed in if async_method is set to True.

        """
        if not async_method:
            method(self.__login_payload)
        else:
            if not loop:
                raise SomethingWentWrong("No Loop was passed in for log in. Will not attempt to search for loop.")
            loop.create_task(method(self.__login_payload))

    def _set_refresh_token(self, refresh_token: str):
        """
        Set the refresh token.

        Parameters
        ----------
        refresh_token: str
            The refresh token to pass when logging in.
        """
        self.__login_payload["refresh_token"] = refresh_token

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
