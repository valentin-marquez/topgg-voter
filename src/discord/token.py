"""
Token class utility.
"""

class Token:
    """
    Token class for encrypting and decrypting Tokens.
    """

    def __init__(self, token: str):
        self._token = token

    def censored(self):
        """
        Censor token.
        """
        return self._token.replace(self._token[0:10], "**********")

    @property
    def value(self):
        """
        Get token.
        """
        return self._token
