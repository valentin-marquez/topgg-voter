"""
Miscellaneous functions.
"""
import os

import requests


def get_version() -> str:
    """
    Gets the current version of the bot.
    """
    return os.environ["VERSION"]


def last_release() -> str:
    """
    Gets the latest release of the bot.
    """
    return requests.get("https://api.github.com/repos/NozzOne/topgg-voter/releases/latest",
                        timeout=5).json()["tag_name"]


def update_available() -> bool:
    """
    Checks if there is an update available.
    """
    return get_version() != last_release()

def can_voted(cookie:str, bots:list) -> list[str]:
    """Check if the user can vote. Returns a list of urls. """
    urls = []
    for bot_id in bots:
        cookies = {"connect.sid": cookie}
        url = f'https://top.gg/api/client/discord/bot/{bot_id}/vote/check'
        request = requests.get(url, cookies=cookies, timeout=5)

        if request.json()['status']:
            urls.append('https://top.gg/bot/' + bot_id + '/vote')
        elif request.json()['status'] == "invalid":
            raise ValueError("Cookie Expired!")
    return urls
