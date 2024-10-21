from .gui import BrowserGUI

class Browser:
    def __init__(self):
        self.gui = BrowserGUI(self)

    def run(self):
        self.gui.run()

    def navigate(self, url):
        self.gui.navigate(url)
