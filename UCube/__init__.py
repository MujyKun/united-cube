from . import models

from .error import InvalidToken, PageNotFound, BeingRateLimited, \
    SomethingWentWrong, InvalidCredentials, LoginFailed, NoHookFound

from .objects import create_club, create_image, BASE_SITE, create_post, create_video, create_board, create_user, \
    create_notification, create_comment
from functools import wraps
from asyncio import iscoroutinefunction

__title__ = 'UCube'
__author__ = 'MujyKun'
__license__ = 'MIT'
__version__ = '0.0.2.1'


def check_expired_token(func):
    """Decorator to reinstate a token if it is expired."""

    @wraps(func)
    async def wrap_async_function(self=None, *args, **kwargs):
        if self.expired_token:
            if self._refresh_token_exists:
                await self._refresh_token()
            else:
                await self._try_login()
                await self._wait_for_login()  # wait for login or an exception to occur.

        return await func(self, *args, **kwargs)

    @wraps(func)
    def wrap_sync_function(self=None, *args, **kwargs):
        if self.expired_token:
            if self._refresh_token_exists:
                self._refresh_token()
            else:
                self._try_login()
        return func(self, *args, **kwargs)
    return wrap_sync_function if not iscoroutinefunction(func) else wrap_async_function


from .ucubeclient import UCubeClient
from .ucubesync import UCubeClientSync
from .ucubeasync import UCubeClientAsync
