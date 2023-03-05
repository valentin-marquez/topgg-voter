import string
from datetime import datetime

import flet as ft

from src import Chrome
from src.discord import Bot, get_bot
from src.util import Browser, encrypt_cookie, logger


class App(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.storage = None
        self.last_vote = None
        self.chromes: list[Chrome] = []

    def init(self):
        self.bots = [get_bot(id) for id in self.storage.get(
            "bots")] if self.storage.contains_key("bots") else []
        self.cookies = []

        if self.storage.contains_key("cookies"):
            for cookie in self.storage.get("cookies"):
                self.cookies.append(encrypt_cookie(cookie))

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

    def start(self, e):
        if self.bots and self.cookies:
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
        self.start_btn = self.add_container(ft.TextButton(
            "VOTE", on_click=self.start, expand=1, height=40, width=100))
        if self.is_configured:
            self.start_btn.content.content.text = "STARTED..."
            self.start_btn.disabled = True
        return self.start_btn

    def remove_bot(self, sender: ft.ControlEvent):
        self.bots_listview.controls.pop(
            self.bots.index(sender.control.data))
        self.bots.remove(sender.control.data)
        self.on_update()
        self.update()

    def add_bot(self, sender: ft.ControlEvent):
        try:

            if self.bot_field.value not in self.bots and self.bot_field.value != "":
                bot = get_bot(int(self.bot_field.value))
                self.bots.append(bot)
                self.bots_listview.controls.append(self.bot_template(bot))
                self.on_update()
                self.update()
        except ValueError as e:
            logger.error(e)
        except AttributeError as e:
            logger.error(e)

    def bots_lv(self, items: list):

        
        self.bots_listview = ft.ListView(expand=1, spacing=5,
                                         padding=10, auto_scroll=True,
                                         col={"xs": 12})
        for item in items:
            self.bots_listview.controls.append(
                self.bot_template(item)
            )
        return self.bots_listview

    def bot_template(self, item: Bot):
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
                        ft.Text("Bot id: {}".format(
                            item.id), weight=ft.FontWeight.W_300, size=ft.TextThemeStyle.DISPLAY_SMALL, font_family="Manrope-Medium"),
                        ft.Text("Bot Name: {}".format(
                            item.name), weight=ft.FontWeight.W_500, size=ft.TextThemeStyle.DISPLAY_SMALL, font_family="Manrope-Medium"),
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

    def add_container(self, component):
        return ft.Card(content=ft.Container(component))

    def bots_sections(self):
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

    def cookie_template(self, cookie):
        return ft.ResponsiveRow(
            col={"xs": 12},
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(cookie, weight=ft.FontWeight.W_300,
                                size=ft.TextThemeStyle.DISPLAY_SMALL),
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

    def cookies_lv(self, items: list):

        self.cookies_listView = ft.ListView(expand=1, spacing=5,
                                            padding=10, height=150)
        for item in items:
            self.cookies_listView.controls.append(
                self.cookie_template(item)
            )
        return self.cookies_listView

    def add_cookie(self, sender: ft.ControlEvent):
        if self.cookie_field.value in self.cookies:
            return
        if not self.cookie_field.value:
            return
        self.cookies.append(encrypt_cookie(self.cookie_field.value))
        self.cookies_listView.controls.append(
            self.cookie_template(encrypt_cookie(self.cookie_field.value)))
        self.on_update()
        self.update()

    def remove_cookie(self, sender: ft.ControlEvent):
        self.cookies_listView.controls.pop(
            self.cookies.index(sender.control.data))
        self.cookies.remove(sender.control.data)
        self.on_update()
        self.update()

    def cookies_sections(self):
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
        self.storage.set("cookies", self.cookies)
        self.storage.set("bots", [bot.id for bot in self.bots])
        self.storage.set("last_time_voted", self.last_vote.value)

    def on_close(self):
        logger.info("close services...")
        try:
            for chrome in self.chromes:
                chrome.kill()
        except Exception as e:
            logger.warning("Failed to kill process: " + str(e))

        logger.info("Saving changes...")
        self.storage.clear()

        self.storage.set("bots", [bot.id for bot in self.bots])
        self.storage.set("cookies", self.cookies)
        self.storage.set("last_time_voted", self.last_vote.value)
