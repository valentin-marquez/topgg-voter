
import time
from subprocess import CREATE_NO_WINDOW

import requests
import undetected_chromedriver as uc
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.util import (Browser, get_browser, get_chrome_version,
                                  resource_path, logger)


class Chrome:
    def __init__(self, headless, browser, bots: list, cookies: list):
        self.headless = headless
        self.bots = bots
        self.cookies = cookies
        self.browser = browser
        self.driver = uc.Chrome(options=self._options(),
                                desired_capabilities=self._capbilities(), 
                                use_subprocess=True, 
                                browser_executable_path=get_browser(self.browser), 
                                version_main=get_chrome_version(),
                                service_creationflags=CREATE_NO_WINDOW)
        self.ignored_exceptions = (
            NoSuchElementException, StaleElementReferenceException)
        self.wait = WebDriverWait(
            self.driver, 3, ignored_exceptions=self.ignored_exceptions)

    def _capbilities(self):
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = ""
        prox.socks_proxy = ""
        prox.ssl_proxy = ""

        cap = DesiredCapabilities.CHROME

        prox.add_to_capabilities(cap)

        return cap

    def _options(self):

        anticaptcha = resource_path(
            "./assets/extensions/hektCaptcha Extension/")
        ublock = resource_path("./assets/extensions/ublock/")

        options = uc.ChromeOptions()
        options.binary_location = get_browser(self.browser)
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--lang=en-US")
        options.add_argument(f"--load-extension={ublock},{anticaptcha}")
        options.add_argument("--headless=new")

        return options

    def check_hcaptcha(self):

        try:
            self.wait_for(
                "//iframe[@title='Main content of the hCaptcha challenge']")
            iframe = self.driver.find_element(
                By.XPATH, "//iframe[@title='Main content of the hCaptcha challenge']")
            if iframe:
                time.sleep(5)
        except:
            pass

    def wait_for(self, xpath):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except:
            pass

    def vote(self):
        try:
            self.wait_for("//*[contains(text(), 'Vote')]")
            self.driver.find_element(
                By.XPATH, "//*[contains(text(), 'Vote')]").click()
            try:
                self.check_hcaptcha()
            except Exception as e:
                print(e)
                pass
            time.sleep(1)
        except ElementClickInterceptedException:
            pass

    def can_voted(self, cookie):
        urls = []
        for id in self.bots:
            cookies = {"connect.sid": cookie}
            url = f'https://top.gg/api/client/discord/bot/{id}/vote/check'
            r = requests.get(url, cookies=cookies)
            print(f"Bot ID: {id} | Status: {r.json()['status']}")
            if r.json()['status']:
                urls.append('https://top.gg/bot/' + id + '/vote')
            elif r.json()['status'] == "invalid":
                raise Exception("Cookie Expired!")
        return urls

    def process(self, cookie):
        urls = self.can_voted(cookie)
        if len(urls) > 0:
            for i in urls:
                self.driver.get(i)
                self.vote()

    def check_if_closed(self):
        if self.driver.service.process.poll() is not None:
            self.driver.quit()
            logger.info("Chrome Closed!")

    def run(self):
        for cookie in self.cookies:
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
        self.driver.quit()


if __name__ == "__main__":
    Chrome(True, Browser.CHROME).run()
