import os
import sys
import winreg
from enum import Enum


class Browser(Enum):
    CHROME = "chrome.exe"

class REG:
    def handle(self, browser=Browser.CHROME.value):
        try:
            handle = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{}".format(browser))
            return handle
        except:
            return None

    def get_path(self, browser=Browser.CHROME.value):
        try:
            path = winreg.QueryValueEx(self.handle(browser), "Path")[0]
            return path
        except:
            return None

    def get_version(self):
        try:
            handle = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            return winreg.QueryValueEx(handle, "version")[0].split(".")[0]
        except:
            return None

    def get_browser(self, browser: Enum = Browser.CHROME):
        if self.get_path(browser.value):
            return self.get_path(browser.value) + "\\" + browser.value
        else:
            return None


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


REG = REG()
