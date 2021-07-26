import time
import requests.sessions
from typing import Optional, List
from UCube import UCubeClientSync, InvalidToken, BeingRateLimited, models
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
            'username': getenv("UCUBE_USERNAME"),
            'password': getenv("UCUBE_PASSWORD"),
            'token': getenv("UCUBE_AUTH"),
            'verbose': False,
            'web_session': requests.Session()
        }

        self.ucube_client = UCubeClientSync(**kwargs)

    def start(self):
        self.ucube_client.start()


if __name__ == '__main__':
    print("================================")
    print("||Starting Synchronous Example||")
    print("================================")

    load_dotenv()  # load the .env vars -- Important.
    example_object = Example()
    example_object.start()

