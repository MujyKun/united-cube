import aiohttp
from asyncio import get_event_loop
from . import UCubeClient, InvalidToken, InvalidCredentials, SomethingWentWrong


class UCubeClientAsync(UCubeClient):
    r"""
    Asynchronous UCube Client that Inherits from :ref:`UCubeClient`.

    Parameters
    ----------
    loop:
        Asyncio Event Loop
    kwargs:
        Args for :ref:`UCubeClient`.


    Attributes
    -----------
    loop:
        Asyncio Event Loop

    More Attributes can be found in :ref:`UCubeClient`.
    """

    def __init__(self, loop=get_event_loop(), **kwargs):
        self.loop = loop
        super().__init__(**kwargs)

    async def start(self, ):
        """Creates internal cache.

        This is the main process that should be run.

        This is a coroutine and must be awaited.

        :raises: :class:`UCube.error.InvalidToken` If the token was invalid.
        :raises: :class:`UCube.error.InvalidCredentials` If the user credentials were invalid or not provided.
        :raises: :class:`UCube.error.BeingRateLimited` If the client is being rate-limited.
        :raises: :class:`UCube.error.SomethingWentWrong` If Something went wrong. Error explains more.
        """
        try:
            if not self.web_session:
                self.web_session = aiohttp.ClientSession()

            if not self._login_info_exists and not self._token_exists:
                raise InvalidCredentials

            if self._login_info_exists:
                await self.__try_login()

            if not await self.check_token_works():
                raise InvalidToken

            self.cache_loaded = True
        except Exception as err:
            raise err

    async def __try_login(self):
        """
        Will attempt to login to UCube and set refresh token and token.

        This is a coroutine and must be awaited.

        :raises: :class:`UCube.error.InvalidCredentials` If the credentials failed.
        """
        self._login(self.__process_login, async_method=True, loop=self.loop)

    async def __process_login(self, login_payload: dict):
        """
        Will process login credentials and set refresh token and token.

        This is a coroutine and must be awaited.

        Parameters
        ----------
        login_payload: dict
            The client's login payload
        """
        async with self.web_session.post(url=self._auth_login_url, data=login_payload) as resp:
            if self._check_status(resp.status, self._auth_login_url):
                data = await resp.json()
                refresh_token = data.get("refresh_token")
                token = data.get("token")
                if refresh_token:
                    self._set_refresh_token(refresh_token)
                if token:
                    self._set_token(token)
                return
        raise SomethingWentWrong("Login Failed.")

    async def check_token_works(self) -> bool:
        """
        Check if a token is valid and will set the general information about the client if it is.

        This is a coroutine and must be awaited.

        :returns: (:class:`bool`) True if the token works.
        """
        async with self.web_session.get(url=self._about_me_url, headers=self._headers) as resp:
            if resp.status == 200:
                self._set_my_info(await resp.json())
                return True
