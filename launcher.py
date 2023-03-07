"""Launcher for the application."""
import os
import sys
from secrets import token_hex

import flet as ft
from win32com.client import Dispatch

from src.main import main
from src.util.routes import resource_path

os.environ["VERSION"] = "v1.1.0"
os.environ["SECRET"] = token_hex(32)

if __name__ == "__main__":

    shortcut_path = os.path.join(
        os.environ["APPDATA"],
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
        "top.gg voter.lnk")
    target = os.path.abspath(sys.argv[0])
    if not os.path.exists(shortcut_path):
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.save()

    ft.app(target=main, assets_dir=resource_path("assets"))
