# pylint: disable=unused-argument
"""module for core app"""
import string
from datetime import datetime

import flet as ft

from src import Cookie, Chrome
from src.discord import Bot, get_bot
from src.util import Browser, logger


class App(ft.UserControl):
    """
    Main app
    """

    def __init__(self):
        super().__init__()
        self.storage = None
        self.last_vote = None
        self.chromes: list[Chrome] = []
        self.bots: list[Bot] = []
        self.cookies = []
        self.is_configured = False

        # Components
        self.bots_listview = None
        self.cookies_listview = None
        self.start_btn = None
        self.bot_field = None
        self.cookie_field = None

    def init(self):
        """
        Init the app
        """
        self.bots = [get_bot(id) for id in self.storage.get(
            "bots")] if self.storage.contains_key("bots") else []
        self.cookies = []

        if self.storage.contains_key("cookies"):
            for cookie in self.storage.get("cookies"):
                self.cookies.append(Cookie(cookie))

        self.is_configured = True if self.bots and self.cookies else False

    def build(self):
        return ft.Container(
            content=ft.ResponsiveRow(
                expand=True,
                controls=[
                    ft.Text("Bots", text_align="left", font_family="Manrope-Medium",
                            style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight=ft.FontWeight.W_500),
                    self.bots_sections(),
                    self.bots_lv(self.bots),
                    ft.Text("Cookies", text_align="left", font_family="Manrope-Medium",
                            style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight=ft.FontWeight.W_500),
                    self.cookies_sections(),
                    self.cookies_lv(self.cookies),
                    self.start_button()
                ],
            ),
            padding=15
        )

    def start(self, event):
        """
        Start the bot
        """
        if self.bots and self.cookies and not self.chromes:
            self.start_btn.content.content.text = "STARTED..."
            self.start_btn.disabled = True
            self.update()
            driver = Chrome(True, Browser.CHROME,
                            self.storage.get("bots"), self.cookies)
            driver.run()
            self.chromes.append(driver)

            self.storage.set("last_time_voted",
                             datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            self.last_vote.value = self.storage.get('last_time_voted')
            self.start_btn.content.content.text = "VOTE"
            self.start_btn.disabled = False
            self.update()
        else:
            logger.error("No bots or cookies selected")

    def start_button(self) -> ft.Card:
        """Return a component with a button to start the bot
        Returns:
            ft.Card: A material design card
        """
        self.start_btn = self.add_container(ft.TextButton(
            "VOTE", on_click=self.start, expand=1, height=40, width=100))
        if self.is_configured:
            self.start_btn.content.content.text = "STARTED..."
            self.start_btn.disabled = True
        return self.start_btn

    def remove_bot(self, sender: ft.ControlEvent):
        """Remove a bot from the list

        Args:
            sender (ft.ControlEvent): Class that contains the control that triggered the event
        """
        self.bots_listview.controls.pop(
            self.bots.index(sender.control.data))
        self.bots.remove(sender.control.data)
        self.on_update()
        self.update()

    def add_bot(self, event: ft.ControlEvent):
        """Add a bot to the list

        Args:
            sender (ft.ControlEvent): Class that contains the control that triggered the event
        """
        try:

            if self.bot_field.value not in self.bots and self.bot_field.value != "":
                bot = get_bot(int(self.bot_field.value))
                self.bots.append(bot)
                self.bots_listview.controls.append(self.bot_template(bot))
                self.on_update()
                self.update()
        except ValueError as error:
            logger.error(error)
        except AttributeError as error:
            logger.error(error)

    def bots_lv(self, items: list):
        """

        Args:
            items (list): _description_

        Returns:
            _type_: _description_
        """
        self.bots_listview = ft.ListView(expand=1, spacing=5,
                                         padding=10, auto_scroll=True,
                                         height=200, col={"xs": 12})
        for item in items:
            self.bots_listview.controls.append(
                self.bot_template(item)
            )
        return self.bots_listview

    def bot_template(self, item: Bot) -> ft.ResponsiveRow:
        """View of bot information in the list

        Args:
            item (Bot): Bot Object

        Returns:
            ft.ResponsiveRow: Responsive row with the bot information
        """
        return ft.ResponsiveRow(
            col={"xs": 12},
            controls=[
                ft.Column(
                    controls=[
                        ft.Image(src=item.icon,
                                 fit=ft.ImageFit.COVER,
                                 col={"xs": 3},
                                 border_radius=10),
                    ],
                    col={"xs": 2},
                ),
                ft.Column(
                    controls=[
                        ft.Text(f"Bot id: {item.bot_id}", weight=ft.FontWeight.W_300,
                                size=ft.TextThemeStyle.DISPLAY_SMALL, font_family="Manrope-Medium"),
                        ft.Text(f"Bot Name: {item.name}", weight=ft.FontWeight.W_500,
                                size=ft.TextThemeStyle.DISPLAY_SMALL, font_family="Manrope-Medium"),
                    ],
                    col={"xs": 5},
                ),
                ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.ElevatedButton(
                            text="Remove", on_click=self.remove_bot, data=item),
                    ],
                    col={"xs": 5},
                )
            ]
        )

    @classmethod
    def add_container(cls, component) -> ft.Card:
        """Add a container to a component

        Args:
            component (ft.Control): Component to add the container

        Returns:
            ft.Card: A material design card
        """
        return ft.Card(content=ft.Container(component))

    def bots_sections(self) -> ft.Column:
        """Return a component with the bots section

        Returns:
            ft.Column: A material design column
        """
        def numbers_filter(sender: ft.ControlEvent):
            sender.control.value = "".join(
                [c for c in sender.control.value if c in string.digits])
            self.update()

        self.bot_field = ft.TextField(on_change=numbers_filter, height=60)

        return ft.Column(
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        self.bot_field,
                        ft.ElevatedButton(text="Add Bot",
                                          on_click=self.add_bot),
                    ]
                )
            ]
        )

    def cookie_template(self, cookie:Cookie) -> ft.ResponsiveRow:
        """View of cookie information in the list

        Args:
            cookie (str): Cookie string

        Returns:
            ft.ResponsiveRow: Responsive row with the cookie information
        """
        return ft.ResponsiveRow(
            col={"xs": 12},
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(
                            ft.Text(cookie.censored(), weight=ft.FontWeight.W_300,
                                                size=ft.TextThemeStyle.DISPLAY_SMALL),
                            blur=ft.Blur(4,4, ft.BlurTileMode.CLAMP)
                        )
                    ],
                    col={"xs": 7},
                ),
                ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.ElevatedButton(
                            text="Remove", on_click=self.remove_cookie, data=cookie),
                    ],
                    col={"xs": 5},
                )
            ]
        )

    def cookies_lv(self, items: list) -> ft.ListView:
        """Return a listview with the cookies

        Args:
            items (list): Cookies list

        Returns:
            ft.ListView: a listview with the cookies
        """
        self.cookies_listview = ft.ListView(expand=1, spacing=5,
                                            padding=10, height=150)
        for item in items:
            self.cookies_listview.controls.append(
                self.cookie_template(item)
            )
        return self.cookies_listview

    def add_cookie(self, event: ft.ControlEvent):
        """ Add a cookie to the list

        Args:
            sender (ft.ControlEvent): Class that contains the control that triggered the event
        """
        if self.cookie_field.value in self.cookies:
            return
        if not self.cookie_field.value:
            return
        current_cookie = Cookie(self.cookie_field.value)
        self.cookies.append(current_cookie)
        self.cookies_listview.controls.append(
            self.cookie_template(current_cookie))
        self.on_update()
        self.update()

    def remove_cookie(self, sender: ft.ControlEvent):
        """Remove a cookie from the list

        Args:
            sender (ft.ControlEvent): Class that contains the control that triggered the event
        """
        self.cookies_listview.controls.pop(
            self.cookies.index(sender.control.data))
        self.cookies.remove(sender.control.data)
        self.on_update()
        self.update()

    def cookies_sections(self) -> ft.Column:
        """Cookie section

        Returns:
            ft.Column: Cookie section
        """
        self.cookie_field = ft.TextField(
            hint_text="Paste your cookie here", height=60)

        return ft.Column(
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        self.cookie_field,
                        ft.ElevatedButton(text="Add Cookie",
                                          on_click=self.add_cookie),
                    ]
                )
            ]
        )

    def on_update(self):
        """
        handle the update of the data in the storage
        """
        self.storage.set("cookies", self.cookies)
        self.storage.set("bots", [bot.bot_id for bot in self.bots])
        self.storage.set("last_time_voted", self.last_vote.value)

    def on_close(self):
        """
        handle the close of the app
        """
        logger.info("close services...")
        try:
            for chrome in self.chromes:
                chrome.kill()
        except ValueError as error:
            logger.error(error)
        logger.info("Saving changes...")
        self.storage.clear()

        self.storage.set("bots", [bot.bot_id for bot in self.bots])
        self.storage.set("cookies", self.cookies)
        self.storage.set("last_time_voted", self.last_vote.value)
