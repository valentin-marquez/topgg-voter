import pystray
from PIL import Image

from src.util.routes import resource_path


class Tray(pystray.Icon):
    def __init__(self, 
                name="Automatic Voter", 
                icon=Image.open(resource_path("./assets/icons/favicon.png")), 
                title="Automatic Voter",
                menu=None,
                **kwargs):
        super().__init__(name, icon, title, menu, **kwargs)
        
        self.visible = False
        self.run_detached()

    def run_detached(self):
        return super().run_detached(self.visible)
    