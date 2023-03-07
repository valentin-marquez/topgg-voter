"""
This file contains the functions to get bots from the Discord API.
"""
import requests

from src.util import logger


class Bot:
    """
    Bot class for getting bots from the Discord API.

    Attributes:
        id (int): The bot's ID.
        name (str): The bot's name.
        icon (str): The bot's icon.
        is_bot (bool): If the user is a bot.

    Methods:
        from_json(json): Creates a Bot object from a json.
    """

    def __init__(self, bot_id: int, name: str, icon: str, is_bot: bool) -> None:
        self.bot_id = bot_id
        self.name = name
        self.icon = icon
        self.is_bot = is_bot

        if self.icon is None:
            self.icon = "https://discord.com/assets/322c936a8c8be1b803cd94861bdfa868.png"

        if self.is_bot == False:
            raise ValueError("This is not a bot.")

    @classmethod
    def from_json(cls, json):
        try:
            return cls(json["id"], json["name"], json["icon"], json["is_bot"])
        except KeyError as e:
            logger.error(f"Error: {e}")

    def __repr__(self) -> str:
        return f"Bot({self.id}, {self.name}, {self.icon}, {self.is_bot})"

def is_bot(json):
    return False if "code" in json else True


def get_bot(id: int) -> Bot:
    try:
        r = requests.get(
            f"https://discordlookup.mesavirep.xyz/v1/application/{id}")
        if r.status_code == 200:
            json = r.json()
            json["is_bot"] = is_bot(json)
            return Bot.from_json(json)
    except AttributeError:
        logger.error("Error: Connection error")


if __name__ == "__main__":
    bot = get_bot(432610292342587392)
