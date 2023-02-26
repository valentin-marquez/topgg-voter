import os
import sys

import flet as ft
from win32com.client import Dispatch

from src.main import main
from src.util.file_routes import resource_path

VERSION = "v1.0.0"

if __name__ == "__main__":

    shortcut_path = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "top.gg voter.lnk")
    target = os.path.abspath(sys.argv[0])
    if not os.path.exists(shortcut_path):
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.save()

    ft.app(target=main, assets_dir=resource_path("assets"))