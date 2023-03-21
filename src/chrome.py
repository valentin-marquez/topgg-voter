"""
Module for automated voting using Chrome.
"""
import time
import os
from subprocess import CREATE_NO_WINDOW

import undetected_chromedriver as uc
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException,
                                        WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.discord import Tk
from src.util import Google, Browser, can_voted, logger, delete_chromedriver, extension_path


class LocalStorage:
    """Local Storage class for Chrome."""

    def __init__(self, driver: uc.Chrome):
        self.driver: uc = driver

    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self):
        """Returns a list of (key, value) tuples for every entry in local storage"""
        return self.driver.execute_script(
            "var ls = window.localStorage, items = {}; "
            "for (var i = 0, k; i < ls.length; ++i) "
            "  items[k = ls.key(i)] = ls.getItem(k); "
            "return items; ")

    def keys(self):
        """Returns a list of keys in local storage"""
        return self.driver.execute_script(
            "var ls = window.localStorage, keys = []; "
            "for (var i = 0; i < ls.length; ++i) "
            "  keys[i] = ls.key(i); "
            "return keys; ")

    def get(self, key):
        """Returns the value of the given key in local storage, or None if the key does not exist"""
        return self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def set_token(self, token: str):
        """Sets the token prepare for discord"""
        script = 'function login(token) {setInterval(() => {document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`}, 50);setTimeout(() => {location.reload();}, 500);}'
        self.driver.execute_script(script + f'login("{token}")')

    def set(self, key, value):
        """Sets the value of the given key in local storage"""
        self.driver.execute_script(
            "window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        """Returns true if the given key exists in local storage"""
        return key in self.keys()

    def remove(self, key):
        """Removes the given key from local storage"""
        self.driver.execute_script(
            "window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        """Clears all entries in local storage"""
        self.driver.execute_script("window.localStorage.clear();")

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()


class Chrome:
    """
    Chrome class for automated voting
    """
    DELAY = 3

    def __init__(self, headless: bool, browser: Browser, bots: list, tokens: list[Tk]):
        self.headless = headless
        self.bots = bots
        self.tokens = tokens
        self.browser = browser
        self.driver = uc.Chrome(options=self._options(),
                                use_subprocess=True,
                                browser_executable_path=Google.get_browser(
                                    self.browser),
                                version_main=Google.get_version(),
                                service_creationflags=CREATE_NO_WINDOW)
        self.ignored_exceptions = (
            NoSuchElementException, StaleElementReferenceException)
        self.wait = WebDriverWait(
            self.driver, 3, ignored_exceptions=self.ignored_exceptions)
        self.localstorage = LocalStorage(self.driver)

    def _options(self):

        hekt_captcha = extension_path("hektCaptcha")
        ublock = extension_path("ublock")


        options = uc.ChromeOptions()
        options.binary_location = Google.get_browser(self.browser)
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--lang=en-US")
        options.add_argument(f"--load-extension={ublock},{hekt_captcha}")
        options.add_encoded_extension(ublock)
        if self.headless:
            options.add_argument("--headless=new")

        return options

    def check_hcaptcha(self):
        """Check if hcaptcha is present."""
        try:
            self.wait_for(
                "//iframe[@title='Main content of the hCaptcha challenge']")
            iframe = self.driver.find_element(
                By.XPATH, "//iframe[@title='Main content of the hCaptcha challenge']")
            if iframe:
                time.sleep(10)
        except NoSuchElementException:
            return False

    def wait_for(self, xpath: str):
        """Wait for element to be clickable.

        Args:
            xpath (str): Xpath of the element.
        """
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            logger.info("Element not found.")

    def vote(self):
        """Vote for the bot."""
        try:
            self.wait_for("//*[contains(text(), 'Vote')]")
            self.driver.find_element(
                By.XPATH, "//*[contains(text(), 'Vote')]").click()
            self.check_hcaptcha()
            time.sleep(self.DELAY)
        except ElementClickInterceptedException:
            logger.info("Already voted.")

    def process(self, cookie: str):
        """Process the voting.

        Args:
            cookie (str): Cookie of the user.
        """
        try:

            urls = can_voted(cookie, self.bots)
            if len(urls) > 0:
                for i in urls:
                    self.driver.get(i)
                    self.vote()
        except WebDriverException:
            self.kill()
            logger.error("Chrome driver already closed.")

    def login_discord(self, token: str) -> bool:
        """Login to discord."""
        url = r"https://discord.com/oauth2/authorize?scope=identify%20guilds%20email&redirect_uri=https%3A%2F%2Ftop.gg%2Flogin%2Fcallback&response_type=code&client_id=422087909634736160"
        self.driver.get(url)
        self.localstorage.set_token(token)
        self.wait_for("//div[contains(text(), 'Authorize')]")
        self.driver.find_element(By.XPATH, "//div[contains(text(), 'Authorize')]").click()
        time.sleep(3)
        return True

    def run(self):
        """Run the chrome driver."""
        # try:
        # for cookie in self.cookies:
        #     self.driver.get("https://top.gg")
        #     self.driver.add_cookie(
        #         {

        #             'name': 'connect.sid',
        #             'value': cookie.cookie,
        #         }
        #     )
        #     self.driver.refresh()
        #     self.process(cookie.cookie)
        #     self.driver.delete_all_cookies()

        for token in self.tokens:
            if self.login_discord(token.value):
                cookie = self.driver.get_cookie("connect.sid")
                if cookie:
                    self.process(cookie["value"])
        # except WebDriverException:
        #     self.kill()
        #     logger.error("Chrome driver already closed.")

    def kill(self):
        """Kill the chrome driver."""
        try:
            self.driver.quit()
            os.kill(self.driver.browser_pid, 15)
            delete_chromedriver()
        except WebDriverException:
            logger.error("Chrome driver already closed.")
        except PermissionError:
            logger.error("Chrome driver already closed.")
        except OSError:
            logger.error("Chrome driver already killed.")


if __name__ == "__main__":
    chrome = Chrome(False,
                    Browser.CHROME, [432610292342587392],
                    [
                        Tk("Nzc0NDc4NDcyODcyNzIyNDQ0.G_MRpe.SvkThotUBcyDTn_Me5Q-N3bAnib-aD08Jp_UdM")])
    chrome.run()
