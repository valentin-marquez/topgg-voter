"""
Module for automated voting using Chrome.
"""
import time
from subprocess import CREATE_NO_WINDOW

import requests
import undetected_chromedriver as uc
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.cookie import Cookie
from src.util import Google, Browser, resource_path, can_voted


class Chrome:
    """
    Chrome class for automated voting
    """

    def __init__(self, headless, browser: Browser, bots: list, cookies: list[Cookie]):
        self.headless = headless
        self.bots = bots
        self.cookies = cookies
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

    def _options(self):

        anticaptcha = resource_path(
            "./assets/extensions/hektCaptcha Extension/")
        ublock = resource_path("./assets/extensions/ublock/")

        options = uc.ChromeOptions()
        options.binary_location = Google.get_browser(self.browser)
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--lang=en-US")
        options.add_argument(f"--load-extension={ublock},{anticaptcha}")
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
                time.sleep(5)
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
            pass

    def vote(self):
        """Vote for the bot."""
        try:
            self.wait_for("//*[contains(text(), 'Vote')]")
            self.driver.find_element(
                By.XPATH, "//*[contains(text(), 'Vote')]").click()
            self.check_hcaptcha()
            time.sleep(1)
        except ElementClickInterceptedException:
            pass

    def process(self, cookie: str):
        """Process the voting.

        Args:
            cookie (str): Cookie of the user.
        """
        urls = can_voted(cookie)
        if len(urls) > 0:
            for i in urls:
                self.driver.get(i)
                self.vote()

    def run(self):
        """Run the chrome driver."""
        for cookie in self.cookies:
            cookie = cookie.cookie
            self.driver.get("https://top.gg")
            self.driver.add_cookie(
                {

                    'name': 'connect.sid',
                    'value': cookie,
                }
            )
            self.driver.refresh()
            self.process(cookie)
            self.driver.delete_all_cookies()
        self.driver.quit()

    def kill(self):
        """Kill the chrome driver."""
        self.driver.quit()
