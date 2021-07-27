import asyncio
from . import InvalidToken, LoginFailed
from . import BASE_SITE

from typing import Dict, Optional
from .models import Post, Club, Board, User, Notification, Comment


class UCubeClient:
    """
    Abstract & Parent Client for connecting to UCube and creating the internal cache.

    .. warning::
        Do not create an object directly from this class. Instead, create a :class:`UCube.UCubeClientSync` or
        :class:`UCube.UCubeClientAsync` object since those are concrete.

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
    hook:
        A passed in method that will be called every time there is a new notification.
        This method must take in a list of :class:`models.Notification` objects.

    Attributes
    -----------
    verbose: bool
        Whether to print out verbose messages.
    web_session:
        An aiohttp or requests client session.
    cache_loaded: bool
        Whether the Internal UCube Cache is fully loaded.
        This will change for a split moment when grabbing a new post.
    clubs: Dict[:class:`str`, :class:`models.Club`]
        A dict of all Clubs in cache with the slug as the key.
    boards: Dict[:class:`str`, :class:`models.Board`]
        A dict of all Boards in cache with the slug as the key.
    posts: Dict[:class:`str`, :class:`models.Post`]
        A dict of all Posts in cache with the slug as the key.
    users: Dict[:class:`str`, :class:`models.User`]
        A dict of all Users in cache with the slug as the key.
    notifications: Dict[:class:`str`, :class:`models.Notification`]
        A dict of all Notifications in cache with the slug as the key.
   """
    def __init__(self, username: str = None, password: str = None, token=None, web_session=None, verbose: bool = False,
                 hook=None):
        self.verbose = verbose
        self.web_session = web_session

        # we will allow invalid login information until the user uses the start method.
        self.__token = token

        self.__exception_to_raise = None

        self._headers: dict = self.__get_headers()

        self._base_site = BASE_SITE
        self._api_url = self._base_site + "v1/"

        # query string params that we will just append to the URL.
        self._club_slug = "?club={club_slug}"
        self._board_slug = "?board={board_slug}"
        self._per_page_and_number = "per_page={feed_amount}&page={page_number}"

        # slug is the unique identifier that UCube uses for a certain object.
        self._all_clubs_url = self._api_url + "clubs?" + self._per_page_and_number
        self._single_post_url = self._api_url + "posts/{post_slug}"
        self._posts_url = self._api_url + "posts" + "?board={board_slug}&" + self._per_page_and_number
        self._boards_url = self._api_url + "boards" + self._club_slug
        self._feeds_url = self._api_url + "feeds" + self._board_slug + f"&{self._per_page_and_number}"
        self._notifications_url = self._api_url + "notifications" + self._club_slug + f"&{self._per_page_and_number}"
        self._comments_url = self._api_url + "comments?post={post_slug}" + f"&{self._per_page_and_number}&order=desc"

        self._club_info_url = self._api_url + "clubs/{club_slug}"
        self._follow_club_url = self._club_info_url + "/join"
        # to this point, categories has not actually returned any items and is useless.
        self._categories_url = self._api_url + "boards/{club_slug}/categories"

        self._refresh_auth_url = self._api_url + "auth/refresh"
        self._auth_login_url = self._api_url + "auth/login"
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

        # Whether a UCube Client owns the web session or if it belongs to another application.
        self._own_session = False

        self._hook = hook
        self._hook_loop = False

        self.expired_token = False

        self.clubs: Dict[str, Club] = {}
        self.boards: Dict[str, Board] = {}
        self.posts: Dict[str, Post] = {}
        self.users: Dict[str, User] = {}
        self.notifications: Dict[str, Notification] = {}
        self.comments: Dict[str, Comment] = {}

    @property
    def _my_info_exists(self) -> bool:
        return bool(self.__my_info)

    @property
    def _login_info_exists(self) -> bool:
        """Whether login info is present."""
        return self.__login_payload["id"] and self.__login_payload["pw"]

    @property
    def _token_exists(self) -> bool:
        """Whether a token is present."""
        return bool(self.__token)

    @property
    def _refresh_token_exists(self) -> bool:
        """Whether a refresh token is present."""
        return bool(self.__login_payload["refresh_token"])

    def stop(self):
        """Stop the hook loop."""
        self._hook_loop = False

    def _get_refresh_token(self) -> Optional[str]:
        """Get the refresh token."""
        return self.__login_payload["refresh_token"]

    def get_club(self, club_slug: str) -> Optional[Club]:
        """
        Get a Club if it exists.

        Parameters
        ----------
        club_slug: str
            The unique identifier of the Club.

        Returns
        -------
        The Club associated with the slug if it exists.: :class:`models.Club`
        """
        return self.clubs.get(club_slug)

    def get_board(self, board_slug: str) -> Optional[Board]:
        """
        Get a Board if it exists.

        Parameters
        ----------
        board_slug: str
            The unique identifier of the Board.

        Returns
        -------
        The Board associated with the slug if it exists.: :class:`models.Board`
        """
        return self.boards.get(board_slug)

    def get_post(self, post_slug: str) -> Optional[Post]:
        """
        Get a Post if it exists.

        Parameters
        ----------
        post_slug: str
            The unique identifier of the Post.

        Returns
        -------
        The Post associated with the slug if it exists.: :class:`models.Post`
        """
        return self.posts.get(post_slug)

    def get_user(self, user_slug: str) -> Optional[User]:
        """
        Get a User if it exists.

        Parameters
        ----------
        user_slug: str
            The unique identifier of the User.

        Returns
        -------
        The User associated with the slug if it exists.: :class:`models.User`
        """
        return self.users.get(user_slug)

    def get_notification(self, notification_slug: str) -> Optional[Notification]:
        """
        Get a Notification if it exists.

        Parameters
        ----------
        notification_slug: str
            The unique identifier of the Notification.

        Returns
        -------
        The Notification associated with the slug if it exists.: :class:`models.Notification`
        """
        return self.notifications.get(notification_slug)

    def get_comment(self, comment_slug: str) -> Optional[Comment]:
        """
        Get a Comment if it exists.

        Parameters
        ----------
        comment_slug: str
            The unique identifier of the Comment.

        Returns
        -------
        The Comment associated with the slug if it exists.: :class:`models.Comment`
        """
        return self.comments.get(comment_slug)

    async def _wait_for_login(self, timeout=15):
        """
        Will wait until the client is logged in or the timeout timer is exceed.

        Parameters
        ----------
        timeout: int
            Amount of seconds before an exception is raised.

        :raises: :class:`UCube.error.LoginFailed` Login process had failed.
        :raises: :class:`asyncio.exceptions.TimeoutError` Waited too long for a login.
        """
        seconds_passed = 0
        while not self._refresh_token_exists or self.expired_token:
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
            method(self.__login_payload)
        else:
            asyncio.create_task(method(self.__login_payload))

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

    def _set_exception(self, exception: Exception):
        """
        Set an exception from a task that occurred.

        Parameters
        ----------
        exception: The Exception that was raised.
        """
        self.__exception_to_raise = exception

    def _check_status(self, status, url, custom_error_messages: Dict[int, str] = None, message="") -> bool:
        """
        Confirm the status of a URL

        :param status: Status code of url connection
        :param url: Link that we connected to.
        :param custom_error_messages: Any specific error messages for certain statuses.
        :param message: The body message.
        :return: True if the connection was a success.
        :raises: :ref:`invalid_token_exc` if there was an invalid token.
        """
        error_messages = {
            400: "WARNING (NOT CRITICAL): " + url + " was sent a bad request.",
            404: "WARNING (NOT CRITICAL): " + url + " was not found.",
            -1: "WARNING (NOT CRITICAL): " + url + " Failed to load. [Status: " + str(status) + "]"
        }

        if custom_error_messages:
            for key, value in custom_error_messages.items():
                error_messages[key] = value

        error_message = error_messages.get(status)

        if status == 200:
            return True
        elif status == 401 or "Token Expired" in message:
            self.expired_token = True
            # raise InvalidToken
            # InvalidToken no longer needs to be raised due to the next check outside of this function
            # refreshing the login.
        else:
            if not self.verbose:
                return False
            if not error_message:
                error_message = error_messages.get(-1)
            print(error_message)

    def __get_headers(self):
        return {'Authorization': f"Bearer {self.__token}"}
