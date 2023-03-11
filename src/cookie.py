"""
Cookie class for encrypting and decrypting cookies.
"""
import os


class Cookie:
    """
    Cookie class for encrypting and decrypting cookies.
    """

    def __init__(self, cookie: str):
        self._cookie = cookie

    def censored(self):
        """
        Censor cookie.
        """
        return self._cookie.replace(self._cookie[0:10], "**********")

    @property
    def cookie(self):
        """
        Get cookie.
        """
        return self._cookie
