# pylint: disable=unused-argument, disable=global-statement
"""
Main file. This file is the entry point of the application.
"""
import flet as ft
import pystray

from src import App, Background, Tray
from src.util import WindowEventType, resource_path, can_voted

P: ft.Page
voter = App()
scheduler = Background()


def exit_app(icon, query):
    """Exit the application."""
    tray.stop()
    voter.on_close()
    P.window_destroy()
    P.window_close()


def open_app(icon, query):
    """Open the application."""
    tray.visible = False
    P.window_skip_task_bar = False
    P.window_to_front()
    P.update()


def check_vote(icon, query, cookies=None, bots= None):
    """Check if the user can vote."""

    if cookies is None or bots is None:
        return
    vote = []
    for cookie in cookies:
        vote += can_voted(cookie, bots)
    if len(vote) > 0:
        voter.start(event=None)


menu = pystray.Menu(
    pystray.MenuItem("Open", open_app, default=True),
    pystray.MenuItem("Exit", exit_app)
)
tray = Tray(menu=menu)


def on_window_event(event: ft.ControlEvent):
    """Handle window events."""
    if event.data == WindowEventType.MINIMIZE:
        tray.visible = True
        P.window_skip_task_bar = True
        P.update()
    elif event.data == WindowEventType.RESTORE:
        tray.visible = False
        P.window_skip_task_bar = False
        P.update()
    elif event.data == WindowEventType.CLOSE:
        tray.stop()
        voter.on_close()
        P.window_destroy()
        P.window_close()


def main(page: ft.Page):
    """Main function."""
    global P
    P = page
    page.title = "Automatic Voter"
    page.window_width = 640
    page.window_height = 860
    page.window_max_height = 640
    page.window_height = 860
    page.dark_theme = ft.Theme(color_scheme_seed='#ff3366', font_family="Manrope-Regular",
                               visual_density=ft.ThemeVisualDensity.ADAPTIVEPLATFORMDENSITY)
    page.theme_mode = ft.ThemeMode.DARK
    page.window_prevent_close = True
    page.spacing = 0
    page.padding = 0
    page.fonts = {
        "Manrope-Bold": resource_path("./assets/fonts/Manrope-Bold.ttf"),
        "Manrope-ExtraBold": resource_path("./assets/fonts/Manrope-ExtraBold.ttf"),
        "Manrope-ExtraLight": resource_path("./assets/fonts/Manrope-ExtraLight.ttf"),
        "Manrope-Light": resource_path("./assets/fonts/Manrope-Light.ttf"),
        "Manrope-Medium": resource_path("./assets/fonts/Manrope-Medium.ttf"),
        "Manrope-Regular": resource_path("./assets/fonts/Manrope-Regular.ttf"),
        "Manrope-SemiBold": resource_path("./assets/fonts/Manrope-SemiBold.ttf"),
    }

    if page.client_storage.contains_key("last_time_voted"):
        last_time_voted = page.client_storage.get("last_time_voted")
    else:
        last_time_voted = "Never"
    voter.on_start(page.client_storage)
    scheduler.add_job(check_vote, 'interval', minutes=60, args=[tray, None])
    widthsrc = page.width

    page.on_window_event = on_window_event

    text_last_time_voted = ft.Text(last_time_voted, text_align=ft.TextAlign.RIGHT,
                                   color="white", font_family="Manrope-Regular", size=12)
    voter.last_vote = text_last_time_voted
    page.add(
        ft.ResponsiveRow([
            ft.WindowDragArea(
                ft.Container(
                    width=widthsrc,
                    padding=10,
                    content=ft.Row([
                        ft.Column([
                            ft.Text("Last vote:", text_align=ft.TextAlign.RIGHT,
                                    color="white", font_family="Manrope-Regular", size=12),
                            text_last_time_voted,
                        ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Text("ToP.gg Voter", text_align=ft.TextAlign.RIGHT,
                                color="white", font_family="Manrope-SemiBold", size=32),
                        ft.Column(
                            [
                                ft.Text("v1.0.0", text_align=ft.TextAlign.RIGHT,
                                        color="white", font_family="Manrope-Regular", size=12),
                                ft.Text("by: @Nozz#4282", text_align=ft.TextAlign.RIGHT,
                                        color="white", font_family="Manrope-Regular", size=12),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )

                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ),
            )
        ])
    )

    page.add(voter)
    page.update()
    cookies = page.client_storage.get("cookies")
    bots = page.client_storage.get("bots")
    check_vote(tray, None, cookies, bots)
