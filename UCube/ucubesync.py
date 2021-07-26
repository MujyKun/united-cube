import json
import time

import requests
from . import UCubeClient, InvalidToken, InvalidCredentials, LoginFailed, create_club, \
    models, create_post, create_board, create_notification, create_comment, check_expired_token, NoHookFound
from typing import List, Optional
from random import SystemRandom
from string import ascii_letters, digits


class UCubeClientSync(UCubeClient):
    r"""
    Synchronous UCube Client that Inherits from :ref:`UCubeClient`.

    Parameters
    ----------
    kwargs:
        Args for :ref:`UCubeClient`.

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __del__(self):
        """Terminate the web session if it was created by this object."""
        try:
            if self._own_session:
                self.web_session.close()
        except Exception:
            ...

    def start(self, load_boards=True, load_posts=True, load_notices=True, load_media=True,
              load_from_artist=True, load_to_artist=False, load_talk=False, load_comments=False,
              follow_all_clubs=True):
        """Creates internal cache.

        This is the main process that should be run.

        Parameters
        ----------
        load_boards: :class:`bool`
            Whether to load up all of a Club's boards.
        load_posts: :class:`bool`
            Whether to load up all of the Posts of a Board.
        load_notices: :class:`bool`
            Whether to load up all of the Notice posts.
        load_media: :class:`bool`
            Whether to load up all of the Media posts.
        load_from_artist: :class:`bool`
            Whether to load up all of the From Artist posts.
        load_to_artist: :class:`bool`
            Whether to load up all of the To Artist posts.
        load_talk: :class:`bool`
            Whether to load up all of the talk posts.
        load_comments: :class:`bool`
            Whether to load up comments.
        follow_all_clubs: :class:`bool`
            Whether to follow all clubs that are not followed.


        .. warning:: All Clubs and Notifications are always created no matter what.
            The params are dependent on each other. Attempting to
            load ``notices``/``media``/``from artist``/``to artist``/``talk``/``comments`` will not work without
            ``load_posts`` set to ``True``. Attempting to load any posts will not work
            without ``load_boards`` set to ``True``.

        :raises: :class:`UCube.error.InvalidToken` If the token was invalid.
        :raises: :class:`UCube.error.InvalidCredentials` If the user credentials were invalid or not provided.
        :raises: :class:`UCube.error.BeingRateLimited` If the client is being rate-limited.
        :raises: :class:`UCube.error.LoginFailed` Login process had failed.
        """
        try:
            if not self.web_session:
                self.web_session = requests.Session()
                self._own_session = True  # we own the session and need to close it.

            if not self._login_info_exists and not self._token_exists:
                raise InvalidCredentials

            if self._login_info_exists:
                self._try_login()

            if not self.check_token_works():
                raise InvalidToken

            for club in self.fetch_all_clubs():
                if follow_all_clubs:
                    self.follow_club(club.slug)

                club.notifications = self.fetch_club_notifications(club.slug)

                if not load_boards:
                    continue

                for board in self.fetch_club_boards(club.slug):
                    club.boards[board.slug] = board

                    board_name = str(board)

                    # cases to go to the next board.
                    no_notices = not load_notices and board_name == "Notice"
                    no_media = not load_media and board_name == "Media"
                    no_to_artist = not load_to_artist and board_name == f"To {club.artist_name}"
                    no_from_artist = not load_from_artist and board_name == f"From {club.artist_name}"
                    no_talk = not load_talk and board_name == "Talk"

                    if not load_posts or no_notices or no_media or no_to_artist or no_from_artist or no_talk:
                        continue

                    for post in self.fetch_board_posts(board.slug, feed=True):
                        board.posts[post.slug] = post
                        if load_comments:
                            post.comments = self.fetch_post_comments(post.slug)

            self.cache_loaded = True
        except Exception as err:
            if self._own_session:
                self.web_session.close()

            raise err

    def _try_login(self):
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
                self.expired_token = False
                return
        raise LoginFailed

    @check_expired_token
    def fetch_club_boards(self, club_slug: str) -> List[models.Board]:
        """
        Retrieve a list of Boards from a Club.

        Parameters
        ----------
        club_slug: str
            The slug (Unique Identifier) of a Club.

        Returns
        -------
        A list of Boards: List[:class:`models.Board`]
        """
        boards = []
        replace_kwargs = {
            "{club_slug}": club_slug
        }
        url = self.replace(self._boards_url, **replace_kwargs)
        with self.web_session.get(url=url, headers=self._headers) as resp:
            if self._check_status(resp.status_code, url):
                data = json.loads(resp.text)
                for raw_board in data.get("items"):
                    board = create_board(raw_board)
                    boards.append(board)
                    self.boards[board.slug] = board
        return boards

    @check_expired_token
    def fetch_board_posts(self, board_slug: str, feed=False, posts_per_page: int = 99999, page_number: int = 1) \
            -> List[models.Post]:
        """
        Retrieve a list of Posts from a board.

        Parameters
        ----------
        board_slug: str
            The slug (unique identifier) of a board to search the feed for.
        feed: bool
            Whether to use the feeds endpoint. The feeds endpoint would retrieve the user information of a post.
        posts_per_page: int
            The amount of posts to retrieve per page.
        page_number: int
            The page number when paginating.

        Returns
        -------
        A list of Posts: List[:class:`models.Post`]
        """
        posts = []
        replace_kwargs = {
            "{board_slug}": board_slug,
            "{feed_amount}": str(posts_per_page),
            "{page_number}": str(page_number)
        }
        url = self.replace(self._posts_url if not feed else self._feeds_url, **replace_kwargs)
        with self.web_session.get(url=url, headers=self._headers) as resp:
            if self._check_status(resp.status_code, url):
                data = json.loads(resp.text)
                for raw_post in data.get("items"):
                    post = create_post(raw_post)
                    posts.append(post)
                    if post.user:
                        self.users[post.user.slug] = post.user
                    self.posts[post.slug] = post
        return posts

    @check_expired_token
    def fetch_club_notifications(self, club_slug: str, notifications_per_page: int = 99999,
                                 page_number: int = 1) -> List[models.Notification]:
        """
        Retrieve a list of Notifications from a club.

        Parameters
        ----------
        club_slug: str
            The slug (unique identifier) of a club to search the notifications for.
        notifications_per_page: int
            The amount of notifications to retrieve per page.
        page_number: int
            The page number when paginating.

        Returns
        -------
        A list of Notifications: List[:class:`models.Notification`]
        """
        notifications = []
        replace_kwargs = {
            "{club_slug}": club_slug,
            "{feed_amount}": str(notifications_per_page),
            "{page_number}": str(page_number)
        }
        url = self.replace(self._notifications_url, **replace_kwargs)
        with self.web_session.get(url=url, headers=self._headers) as resp:
            if self._check_status(resp.status_code, url):
                data = json.loads(resp.text)
                for raw_notification in data.get("items"):
                    notification = create_notification(raw_notification)
                    notifications.append(notification)
                    self.notifications[notification.slug] = notification
        return notifications

    @check_expired_token
    def fetch_post_comments(self, post_slug: str, comments_per_page: int = 99999,
                            page_number: int = 1) -> List[models.Comment]:
        """
        Retrieve a list of Comments from a Post.

        Parameters
        ----------
        post_slug: str
            The slug (unique identifier) of a Post to search the Comments for.
        comments_per_page: int
            The amount of notifications to retrieve per page.
        page_number: int
            The page number when paginating.

        Returns
        -------
        A list of Comments: List[:class:`models.Comment`]
        """
        comments = []
        replace_kwargs = {
            "{post_slug}": post_slug,
            "{feed_amount}": str(comments_per_page),
            "{page_number}": str(page_number)
        }
        url = self.replace(self._comments_url, **replace_kwargs)
        with self.web_session.get(url=url, headers=self._headers) as resp:
            if self._check_status(resp.status_code, url):
                data = json.loads(resp.text)
                for raw_comment in data.get("items"):
                    comment = create_comment(raw_comment)
                    comments.append(comment)
                    self.comments[comment.slug] = comment
        return comments

    @check_expired_token
    def fetch_post(self, post_slug: str, load_comments=False) -> Optional[models.Post]:
        """
        Fetch a Post by it's slug.

        Parameters
        ----------
        post_slug: :class:`str`
            The post's unique identifier.
        load_comments: :class:`bool`
            Whether to load up the comments of the Post.

        Returns
        -------
        The Post Object if there is one.: :class:`models.Post`

        """
        replace_kwargs = {
            "post_slug": post_slug
        }
        url = self.replace(self._single_post_url, **replace_kwargs)
        with self.web_session.get(url=url, headers=self._headers) as resp:
            if self._check_status(resp.status_code, url):
                raw_post = json.loads(resp.text)
                post = create_post(raw_post)
                if load_comments:
                    post.comments = self.fetch_post_comments(post.slug)
                self.posts[post.slug] = post
                return post
        return

    @check_expired_token
    def fetch_all_clubs(self, clubs_per_page: int = 99999, page_number: int = 1) -> List[models.Club]:
        """
        Fetch all Clubs from the UCube API.

        Returns
        -------
        A list of Clubs: List[:class:`models.Club`]
        """
        clubs = []

        replace_kwargs = {
            "{feed_amount}": str(clubs_per_page),
            "{page_number}": str(page_number)
        }
        url = self.replace(self._all_clubs_url, **replace_kwargs)
        with self.web_session.get(url=url, headers=self._headers) as resp:
            if self._check_status(resp.status_code, url):
                data = json.loads(resp.text)
                for raw_club in data.get("items"):
                    club = create_club(raw_club)
                    clubs.append(club)
                    self.clubs[club.slug] = club
        return clubs

    @check_expired_token
    def follow_club(self, club_slug: str) -> bool:
        """
        Follow a club.

        Parameters
        ----------
        club_slug: :class:`str`
            The unique identifier of the club to follow.

        Returns
        -------
        Whether following the Club was successful.: :class:`bool`

        """
        replace_kwargs = {
            "{club_slug}": club_slug,
        }
        payload = {
            "nick_name": ''.join(SystemRandom().choice(ascii_letters + digits) for _ in range(10))
        }
        url = self.replace(self._follow_club_url, **replace_kwargs)
        headers = self._headers
        with self.web_session.post(url=url, headers=headers, json=payload) as resp:
            custom_error_message = {400: f"WARNING (NOT CRITICAL): Could not follow Club Slug: {club_slug} either due "
                                         f"to a bad argument or they are already being followed."}
            return self._check_status(resp.status_code, url, custom_error_message)

    @check_expired_token
    def check_new_notifications(self) -> List[models.Notification]:
        """
        Checks and returns new notifications for every club.

        Compares with the already existing notifications.
        This will also create the posts associated with the notification so they can be used efficiently.

        Returns
        -------
        A list of new Notifications.: List[:class:`models.Notification`]
        """
        all_new_notifications = []
        for club in self.clubs.values():
            notifications = self.fetch_club_notifications(club.slug, notifications_per_page=15)
            new_notifications = [notification for notification in notifications if notification not in
                                 club.notifications]
            all_new_notifications = all_new_notifications + new_notifications
            club.notifications = club.notifications + new_notifications

            for notification in new_notifications:
                if notification.post_slug:
                    # will add new Post to cache if it exists.
                    self.fetch_post(notification.post_slug)
        return all_new_notifications

    def _start_loop_for_hook(self):
        """
        Start checking for new notifications in a new loop and call the hook with the list of new Notifications

        This will also create the posts associated with the notification so they can be used efficiently.
        """
        if not self._hook:
            raise NoHookFound

        self._hook_loop = True
        while self._hook_loop:
            time.sleep(25)
            new_notifications = self.check_new_notifications()
            if not new_notifications:
                continue

            self._hook(new_notifications)

    def _refresh_token(self):
        """
        Refresh a token while logged in.
        """
        payload = {"refresh_token": self._get_refresh_token()}
        with self.web_session.post(url=self._auth_login_url, json=payload) as resp:
            if self._check_status(resp.status_code, self._auth_login_url):
                data = json.loads(resp.text)
                token = data.get("token")
                if token:
                    self._set_token(token)
                self.expired_token = False
                return
        raise LoginFailed

    def check_token_works(self):
        """
        Check if a token is valid and will set the general information about the client if it is.

        :returns: (:class:`bool`) True if the token works.
        """
        with self.web_session.get(url=self._about_me_url, headers=self._headers) as resp:
            if resp.status_code == 200:
                if not self._my_info_exists:
                    self._set_my_info(json.loads(resp.text))
                return True
