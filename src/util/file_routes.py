import os
import sys
import winreg
from enum import Enum
from typing import Literal


class BrowserNames(Enum):
    EDGE = "Microsoft Edge"
    CHROME = "Google Chrome"
    FIREFOX = "Mozilla Firefox"
    OPERA = "Opera"
    BRAVE = "Brave"
    

class Browser(Enum):
    EDGE = "msedge.exe"
    CHROME = "chrome.exe"
    FIREFOX = "firefox.exe"
    OPERA = "launcher.exe"
    BRAVE = "brave.exe"


    @classmethod
    def parse(cls, browser: str) -> Literal["msedge.exe", "chrome.exe", "firefox.exe", "launcher.exe"]:
        if browser == "msedge.exe":
            return cls.EDGE
        elif browser == "chrome.exe":
            return cls.CHROME
        elif browser == "firefox.exe":
            return cls.FIREFOX
        elif browser == "launcher.exe":
            return cls.OPERA
        elif browser == "brave.exe":
            return cls.BRAVE
        else:
            raise ValueError(f"Invalid browser name: {browser}")

class SystemVariables:

    @property
    def username(self) -> str:
        return os.getenv('USERNAME')

    @property
    def localappdata(self) -> str:
        return os.getenv('LOCALAPPDATA')


class Google:

    def get_profile_number(self) -> str:
        gfolder = self.google_folder

        # check if "default folder" exists in google folder
        if os.path.exists(os.path.join(gfolder, 'Default')):
            return 'Default'
        else:
            # if not, check if there is a folder with a number
            for folder in os.listdir(gfolder):
                if folder.isnumeric():
                    return folder
            else:
                raise FileNotFoundError(
                    f'Could not find profile folder in {gfolder}')

    @property
    def google_folder(self) -> str:
        return os.path.join(SystemVariables.localappdata, f'Google/Chrome/User Data/')

    @property
    def cookies(self) -> str:
        if os.path.exists(os.path.join(self.google_folder, self.get_profile_number(), 'Network')):
            return os.path.join(self.google_folder, self.get_profile_number(), 'Network/Cookies')
        elif os.path.exists(os.path.join(self.google_folder, self.get_profile_number(), 'Cookies')):
            return os.path.join(self.google_folder, self.get_profile_number(), 'Cookies')
        else:
            raise FileNotFoundError(
                f'Could not find cookies file in {self.google_folder}')

    @property
    def localstate(self) -> str:
        return os.path.join(self.google_folder, 'Local State')


class REG:

    def handle(self, browser):
        try:
            handle = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{}".format(browser))
            return handle
        except:
            return None

    def get_path(self, browser):
        try:
            path = winreg.QueryValueEx(self.handle(browser), "Path")[0]
            return path
        except:
            return None
        
    def get_version(self, browser):
        try:
            version = winreg.QueryValueEx(self.handle(browser), "Version")[0]
            return version
        except:
            return None


def get_browser(browser: Enum):
    if REG.get_path(browser.value):
            return REG.get_path(browser.value) + "\\" + browser.value
    else:
        return None

def get_available_browsers():
    browsers = []
    for browser in Browser:
        if get_browser(browser):
            browsers.append(browser.value)

    return browsers

def get_available_browser_names():
    browsers = []
    for browser in Browser:
        if get_browser(browser):
            browsers.append(BrowserNames[browser.name].value)
    return browsers

def get_all_info():
    return zip(get_available_browser_names(), get_available_browsers())

def get_chrome_version():
    try:
        handle = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
        return winreg.QueryValueEx(handle, "version")[0].split(".")[0]
    except:
        return None

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


Google = Google()
SystemVariables = SystemVariables()
REG = REG()