

import flet as ft
import pystray

from src import App, Background, Tray
from src.util import WindowEventType, resource_path

p: ft.Page
voter = App()
scheduler = Background()


def exit_app(icon, query):
    tray.stop()
    voter.on_close()
    p.window_destroy()
    p.window_close()


def open_app(icon, query):
    tray.visible = False
    p.window_skip_task_bar = False

    p.window_always_on_top = True
    p.update()


def check_vote(icon, query):
    if voter.is_configured:
        voter.start(e=None)


menu = pystray.Menu(
    pystray.MenuItem("Open", open_app, default=True),
    pystray.MenuItem("Vote", check_vote),
    pystray.MenuItem("Exit", exit_app)
)
tray = Tray(menu=menu)


def on_window_event(e: ft.ControlEvent):
    if e.data == WindowEventType.MINIMIZE:
        tray.visible = True
        p.window_skip_task_bar = True
        p.update()
    elif e.data == WindowEventType.RESTORE:
        tray.visible = False
        p.window_skip_task_bar = False
        p.update()
    elif e.data == WindowEventType.CLOSE:
        tray.stop()
        voter.on_close()
        p.window_destroy()
        p.window_close()


def main(page: ft.Page):
    global p
    p = page
    page.title = "Automatic Voter"
    page.window_width = 640
    page.window_height = 860
    page.window_max_height = 640
    page.window_height = 860
    page.fonts = {
        "Manrope-Bold": resource_path("./assets/fonts/Manrope-Bold.ttf"),
        "Manrope-ExtraBold": resource_path("./assets/fonts/Manrope-ExtraBold.ttf"),
        "Manrope-ExtraLight": resource_path("./assets/fonts/Manrope-ExtraLight.ttf"),
        "Manrope-Light": resource_path("./assets/fonts/Manrope-Light.ttf"),
        "Manrope-Medium": resource_path("./assets/fonts/Manrope-Medium.ttf"),
        "Manrope-Regular": resource_path("./assets/fonts/Manrope-Regular.ttf"),
        "Manrope-SemiBold": resource_path("./assets/fonts/Manrope-SemiBold.ttf"),
    }
    page.dark_theme = ft.Theme(color_scheme_seed='#ff3366', font_family="Manrope-Regular",
                               visual_density=ft.ThemeVisualDensity.ADAPTIVEPLATFORMDENSITY)
    page.theme_mode = ft.ThemeMode.DARK
    page.window_prevent_close = True
    page.spacing = 0
    page.padding = 0

    if page.client_storage.contains_key("last_time_voted"):
        last_time_voted = page.client_storage.get("last_time_voted")
    else:
        last_time_voted = "Never"
    voter.storage = page.client_storage
    voter.init()
    scheduler.add_job(check_vote, 'interval', minutes=1, args=[tray, None])
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
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Text("Top.gg Voter", text_align=ft.TextAlign.RIGHT,
                                color="white", font_family="Manrope-SemiBold", size=32),
                        ft.Column(
                            [
                                ft.Text("v1.0.0", text_align=ft.TextAlign.RIGHT,
                                        color="white", font_family="Manrope-Regular", size=12),
                                ft.Text("by: @Nozz#4282", text_align=ft.TextAlign.RIGHT,
                                        color="white", font_family="Manrope-Regular", size=12),
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )

                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ),
            )
        ])
    )

    page.add(voter)
    page.update()
    check_vote(tray, None)  # check_vote
