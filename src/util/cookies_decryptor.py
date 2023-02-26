import base64
import logging
import sqlite3
from os import getenv
from shutil import copyfile

import ujson as json
from Cryptodome.Cipher import AES
from win32 import win32crypt

from .file_routes import Google

copyfile(Google.cookies, 'cookies')

class CookiesDecrypt:
    def __init__(self):
        self.conn = sqlite3.connect("cookies")
        self.cursor = self.conn.cursor()
        self.encryption_key = self.get_encryption_key()

    def get_encryption_key(self):
        with open(Google.localstate, 'r', encoding='utf-8') as f:
            encrypted_key = json.loads(f.read())['os_crypt']['encrypted_key']
        encrypted_key = base64.b64decode(encrypted_key)
        encrypted_key = encrypted_key[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    

    def get_cookies(self):
        self.cursor.execute('DELETE FROM cookies WHERE host_key NOT LIKE "%top.gg%"')
        self.conn.commit()
        self.cursor.execute(
            'SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE "%top.gg%"')
        for host_key, name, encrypted_value in self.cursor.fetchall():
            decrypted_value = self.decrypt(encrypted_value)
            if decrypted_value:
                logging.info(f'[COOKIESDECRYPT] {host_key} {name} {decrypted_value}')

                self.cursor.execute('\
                    UPDATE cookies SET value = ?, has_expires = 1, expires_utc = 99999999999999999, is_persistent = 1, is_secure = 0\
                    WHERE host_key = ?\
                    AND name = ?',
                    (decrypted_value, host_key, name))
                

    def decrypt(self, encrypted_value):
        try:
            cipher = AES.new(self.encryption_key, AES.MODE_GCM,
                             encrypted_value[3:3+12])
            decrypted_value = cipher.decrypt_and_verify(
                encrypted_value[3+12:-16], encrypted_value[-16:])
        except:
            decrypted_value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[
                1].decode('utf-8') or encrypted_value or 0

        return decrypted_value

    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    CookiesDecrypt().get_cookies()
