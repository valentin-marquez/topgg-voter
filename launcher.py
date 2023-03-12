"""Launcher for the application."""
import os
import sys
import secrets
import ctypes
import webbrowser

import flet as ft
from win32com.client import Dispatch

from src.main import main
from src.util import update_available, resource_path

os.environ["VERSION"] = "v1.1.0"
os.environ["SECRET"] = secrets.token_hex(16)

if __name__ == "__main__":
    if update_available():
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None,
                "An update is available. Please download it from the repo.",
                "Update available", 0)
        webbrowser.open("https://github.com/NozzOne/topgg-voter/releases/latest")

    else:
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

            os.system(f"mklink {shortcut_path} {target}")

        ft.app(target=main, assets_dir=resource_path("assets"))