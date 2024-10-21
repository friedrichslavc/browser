import asyncio
import logging
from urllib.parse import urlparse
from .network import NetworkManager
from .html_parser import HTMLParser
from .dns_resolver import DNSResolver
from .cache import Cache
from .bookmarks import BookmarkManager
from .history import HistoryManager

class Browser:
    def __init__(self):
        self.network = NetworkManager()
        self.html_parser = HTMLParser()
        self.dns_resolver = DNSResolver()
        self.cache = Cache()
        self.bookmark_manager = BookmarkManager()
        self.history = HistoryManager()
        self.current_url = None
        self.set_content_security_policy()
        self.gui = None  # We'll set this later

    def set_gui(self, gui):
        self.gui = gui

    async def navigate(self, url):
        try:
            content = await self.network.fetch(url)
            await self.history.add_to_history(url)  # 确保这行代码被执行
            self.current_url = url
            logging.info(f"Navigated to: {url}")
            return content
        except Exception as e:
            logging.error(f"Error navigating to {url}: {str(e)}")
            return f"<h1>Error</h1><p>Failed to load {url}: {str(e)}</p>"

    def set_content_security_policy(self):
        self.csp = {
            'default-src': ["'self'"],
            'script-src': ["'self'", "'unsafe-inline'"],
            'style-src': ["'self'", "'unsafe-inline'"],
            'img-src': ["'self'", 'data:', 'https:'],
            'connect-src': ["'self'"],
            'font-src': ["'self'"],
            'object-src': ["'none'"],
            'media-src': ["'self'"],
            'frame-src': ["'self'"],
        }

    def apply_csp(self, url):
        domain = urlparse(url).netloc
        for directive, sources in self.csp.items():
            if domain not in sources and '*' not in sources:
                sources.append(domain)

    async def go_back(self):
        previous_url = await self.history.go_back()
        if previous_url:
            await self.navigate(previous_url)
        else:
            await self.gui.display_error("No previous page in history")

    async def go_forward(self):
        next_url = await self.history.go_forward()
        if next_url:
            await self.navigate(next_url)
        else:
            await self.gui.display_error("No next page in history")

    def add_bookmark(self, title, url):
        self.bookmark_manager.add_bookmark(title, url)
        logging.info(f"Browser: Added bookmark {title} - {url}")

    def get_bookmarks(self):
        return self.bookmark_manager.get_bookmarks()

    def get_history(self):
        history = self.history.get_history()
        logging.info(f"Retrieved history: {history}")
        return history

    def get_current_url(self):
        return self.current_url

    async def search(self, query):
        search_url = f"https://www.google.com/search?q={query}"
        await self.navigate(search_url)

    async def run(self):
        try:
            self.gui.show()
        except Exception as e:
            print(f"An error occurred in the browser: {str(e)}")
        finally:
            await self.cleanup()

    async def cleanup(self):
        await self.network.close_session()

async def main():
    browser = Browser()
    from .gui import BrowserGUI  # 移动到这里以避免循环导入
    gui = BrowserGUI(browser)
    browser.set_gui(gui)
    try:
        await browser.run()
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
