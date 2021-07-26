import requests.sessions
from typing import List

import UCube
from UCube import UCubeClientSync
from dotenv import load_dotenv
from os import getenv

"""
synchronous.py


Synchronous Example for UCube.

This file should be able to run if a token or a username and password is supplied.
If you would like to view more specific information,
then it would be suggested to look at the API Docs at https://ucube.readthedocs.io/en/latest/
or run this file in a debugger.
In order to get a token: https://ucube.readthedocs.io/en/latest/api.html#get-account-token

In order to set a username and password (RECOMMENDED), Rename .env.example to .env and set UCUBE_USERNAME to 
the username and UCUBE_PASSWORD to the password.

In order to set a token (NOT RECOMMENDED - will expire quickly), 
Rename .env.example to .env and set UCUBE_AUTH to the token. 

Before running this file, confirm that you used `pip install -r requirements.txt` in the examples directory.

If you are running in an Asynchronous environment, go take a look at the Asynchronous examples file.

"""


def get_formatted_time(seconds):
    """Turn seconds into days, hours, minutes, and seconds.

    Not related to UCube.
    :param seconds: Amount of seconds to convert.
    """
    seconds = round(seconds)
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)

    return f"{f'{day}d ' if day else ''}" \
           f"{f'{hour}h ' if hour else ''}" \
           f"{f'{minute}m ' if minute else ''}" \
           f"{f'{sec}s' if sec else ''}" \
           f"{f'0s' if seconds < 1 else ''}"


class Example:
    def __init__(self):
        kwargs = {
            # Only pass in the authorization method you plan to use
            # you can choose between passing in a username and password or by putting a token.
            # If you put both, it will prioritize username & password login and create tokens from that.
            'username': getenv("UCUBE_USERNAME"),  # ucube username
            'password': getenv("UCUBE_PASSWORD"),  # ucube password
            'token': getenv("UCUBE_AUTH"),  # not suggested to pass in a token. This token will expire very quickly.
            # verbose will not go to a logger, but just print messages for more info. Should usually set to False.
            'verbose': True,
            'web_session': requests.sessions.Session(),
            'hook': self.on_new_notifications  # SET THIS TO YOUR OWN METHOD TO RECEIVE NEW NOTIFICATIONS

            # It is not necessary to use a hook as you can manually create the loop if you want. However, as it's not
            # recommended, an example won't be shown for that. If you're curious about doing so,
            # you can look into the loop code for the hook and
            # not pass in a hook. (UCube.ucubesync.UCubeClientSync._start_loop_for_hook)
        }

        self.ucube_client = UCubeClientSync(**kwargs)

    def start(self):
        self.ucube_client.start()

        # Create settings for how the history is created.
        # This will create cache for the following:
        # This should be customized to YOUR Client.
        # These settings are just in preference to load up the cache quickly since this example
        # does not need past media/posts/... stored.
        start_kwargs = {
            "load_boards": True,  # loads up all club boards.
            "load_posts": False,  # wouldn't work without load_boards set to True
            "load_notices": False,  # wouldn't work without load_posts set to True
            "load_media": False,  # wouldn't work without load_posts set to True
            "load_from_artist": True,  # wouldn't work without load_posts set to True
            "load_to_artist": False,  # wouldn't work without load_posts set to True
            "load_talk": False,  # wouldn't work without load_posts set to True
            "load_comments": False,  # wouldn't work without load_posts set to True
            "follow_all_clubs": False  # will follow all clubs.
        }
        # login, start loading previous cache (if specified) and set the hook.

        try:
            self.ucube_client.start(**start_kwargs)
        except UCube.InvalidToken:
            print("An Invalid Token was supplied to UCube.")
            ...  # Should consider using credentials instead, tokens expire very quickly.
        except UCube.InvalidCredentials:
            print("An Invalid Username and Password were supplied to UCube.")
            ...  # update the username and password
        except UCube.BeingRateLimited:
            print("UCube was rate-limited at some point. This should usually not occur.")
            ...  # this would be considered an issue with UCube, make an issue on the github repository if this occurs.
        except UCube.LoginFailed:
            print("Failed to log into UCube Client.")
            # You could attempt to reboot, perhaps their server was down or another status error occurred.
            # This issue may occur in a method past the start method. If that is the case, and the cache is already
            # loaded, you can attempt to login and see if that works. This would be considered a manual boot up without
            # resetting the cache of the current client. (Calling the start method again will reset the current cache).
            if self.ucube_client.cache_loaded:
                # you may want to try-except _try_login(), but this example will not contain it for readability
                self.ucube_client._try_login()

                # if we get to this line of code, that means the login was successful.
                # we can now start the hook loop again
                self.ucube_client._start_loop_for_hook()
                # the code should now remain here unless another exception occurs
            ...
        except Exception as e:
            print(f"{e} - UCube Exception")

        # if a hook is passed in,
        # the start method will not reach this point (unless an exception occurs) and will check for new notifications.

    def on_new_notifications(self, notifications: List[UCube.models.Notification]):
        """
        Decides what to do with a list of Notifications.

        This is a hook method. Whenever there is a notification, this method will be called.
        """
        for notification in notifications:
            post = self.ucube_client.get_post(notification.post_slug)
            if not post:
                # you can attempt to fetch the post with:
                # self.ucube_client.fetch_post(notification.post_slug)
                ...
                continue  # skipping the notification - not recommended since you're keeping track of new notifications.
            club = self.ucube_client.get_club(notification.club_slug)  # the club the notification belongs to

            # now that you have the post, you can go ahead and do whatever you want with the object.
            # make sure to READ THE DOCS for specific objects. Search up the Post object if you're interested
            # in things you may be able to do.
            # There is a UCube discord bot (below) if you want to see a real usage.
            # https://github.com/MujyKun/united-cube-bot
            breakpoint()


if __name__ == '__main__':
    print("================================")
    print("||Starting Synchronous Example||")
    print("================================")

    load_dotenv()  # load the .env vars -- Important.
    example_object = Example()
    example_object.start()
