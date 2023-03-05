import os

import requests


def get_version() -> str:
    return os.environ["VERSION"]

def last_release() -> str:
    return requests.get("https://api.github.com/repos/NozzOne/topgg-voter/releases/latest").json()["tag_name"]

def update_available() -> bool:
    return get_version() != last_release()

def encrypt_cookie(cookie):
    secret = os.environ["SECRET"]
    return cookie.encode("utf-8").hex() + secret

def decrypt_cookie(cookie):
    secret = os.environ["SECRET"]
    return bytes.fromhex(cookie[:-len(secret)]).decode("utf-8")
