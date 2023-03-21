"""File routes for the application."""
import os
import sys
import winreg
import zipfile
from enum import Enum


class Browser(Enum):
    """Enum for browser names."""
    CHROME = "chrome.exe"


class Google:
    """
    Class for getting browser paths.
    """

    @classmethod
    def handle(cls, browser=Browser.CHROME.value):
        """Get the handle for the browser."""
        try:
            handle = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                fr"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{browser}")
            return handle
        except OSError:
            return None

    @classmethod
    def get_path(cls, browser=Browser.CHROME.value) -> str:
        """Get the path for the browser.
        Args:
            browser (_type_, optional): Defaults to Browser.CHROME.value.

        Returns:
            str: Path to the browser.
        """
        try:
            path = winreg.QueryValueEx(cls.handle(browser), "Path")[0]
            return path
        except OSError:
            return None

    @classmethod
    def get_version(cls):
        """Get the version of the browser."""
        try:
            handle = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            return winreg.QueryValueEx(handle, "version")[0].split(".")[0]
        except OSError:
            return None

    @classmethod
    def get_browser(cls, browser: Enum = Browser.CHROME) -> str:
        """Get the path to the browser.
        Args:
            browser (Enum, optional): Defaults to Browser.CHROME.

        Returns:
            str: Path to the browser.
        """
        if cls.get_path(browser.value):
            return cls.get_path(browser.value) + "\\" + browser.value
        else:
            return None


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    base_path = getattr(sys, '_MEIPASS', os.getcwd())
    return os.path.join(base_path, relative_path)


def unzip_extensions() -> bool:
    """Unzip the extensions .zip"""

    if not os.path.exists(os.path.join(os.environ["APPDATA"], "Top.gg Voter", "extensions")):
        os.makedirs(os.path.join(
            os.environ["APPDATA"], "Top.gg Voter", "extensions"))
    else:
        return False
    for file in os.listdir(resource_path("assets/extensions")):
        if file.endswith(".zip"):
            with zipfile.ZipFile(resource_path(f"assets/extensions/{file}"), "r") as zip_ref:
                zip_ref.extractall(os.path.join(
                    os.environ["APPDATA"], "Top.gg Voter", "extensions", file[:-4]))
    return True

def extension_path(extension: str) -> str:
    return os.path.join(os.environ["APPDATA"], "Top.gg Voter", "extensions", extension)
