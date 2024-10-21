import asyncio
import sys
from PyQt5.QtWidgets import QApplication
from backend.browser import Browser
from backend.gui import BrowserGUI

async def main():
    app = QApplication(sys.argv)
    browser = Browser()
    gui = BrowserGUI(browser)
    browser.set_gui(gui)
    await browser.run()
    sys.exit(app.exec_())

if __name__ == "__main__":
    asyncio.run(main())
