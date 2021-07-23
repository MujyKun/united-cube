import json
import requests
from . import UCubeClient, InvalidToken, InvalidCredentials, LoginFailed


class UCubeClientSync(UCubeClient):
    r"""
    Synchronous UCube Client that Inherits from :ref:`UCubeClient`.

    Parameters
    ----------
    kwargs:
        Same as :ref:`UCubeClient`.


    Attributes are the same as :ref:`UCubeClient`.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start(self):
        """Creates internal cache.

        This is the main process that should be run.

        :raises: :class:`UCube.error.InvalidToken` If the token was invalid.
        :raises: :class:`UCube.error.InvalidCredentials` If the user credentials were invalid or not provided.
        :raises: :class:`UCube.error.BeingRateLimited` If the client is being rate-limited.
        :raises: :class:`UCube.error.LoginFailed` Login process had failed.
        :raises: :class:`asyncio.exceptions.TimeoutError` Waited too long for a login.
        """
        try:
            if not self.web_session:
                self.web_session = requests.Session()
                self._own_session = True  # we own the session and need to close it.

            if not self._login_info_exists and not self._token_exists:
                raise InvalidCredentials("The credentials for a token or a username/password could not be found.")

            if self._login_info_exists:
                self.__try_login()

            if not self.check_token_works():
                raise InvalidToken

            self.cache_loaded = True
        except Exception as err:
            if self._own_session:
                self.web_session.close()

            raise err

    def __try_login(self):
        """
        Will attempt to login to UCube and set refresh token and token.

        :raises: :class:`UCube.error.LoginFailed` If the login failed.
        """
        self._login(self.__process_login)

    def __process_login(self, login_payload: dict):
        """
        Will process login credentials and set refresh token and token.

        Parameters
        ----------
        login_payload: dict
            The client's login payload
        """
        with self.web_session.post(url=self._auth_login_url, json=login_payload) as resp:

            if self._check_status(resp.status_code, self._auth_login_url):
                data = json.loads(resp.text)
                refresh_token = data.get("refresh_token")
                token = data.get("token")
                if refresh_token:
                    self._set_refresh_token(refresh_token)
                if token:
                    self._set_token(token)
                return

        raise LoginFailed()

    def check_token_works(self):
        """
        Check if a token is valid and will set the general information about the client if it is.

        :returns: (:class:`bool`) True if the token works.
        """
        with self.web_session.get(url=self._about_me_url, headers=self._headers) as resp:
            if resp.status_code == 200:
                self._set_my_info(json.loads(resp.text))
                return True
