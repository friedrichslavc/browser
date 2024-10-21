import requests
from requests.exceptions import RequestException
import ssl
import logging
import asyncio
import aiohttp

class NetworkManager:
    def __init__(self):
        self.session = None

    def send_request(self, url, method='GET', data=None, headers=None):
        try:
            response = requests.request(
                method,
                url,
                data=data,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.text
        except RequestException as e:
            logging.error(f"Request failed: {str(e)}")
            return f"Error: {str(e)}"

    def set_proxy(self, proxy):
        requests.Session().proxies = {'http': proxy, 'https': proxy}

    def disable_ssl_verification(self):
        requests.packages.urllib3.disable_warnings()

    def set_timeout(self, timeout):
        pass

    def clear_cookies(self):
        requests.Session().cookies.clear()

    def set_user_agent(self, user_agent):
        requests.Session().headers.update({'User-Agent': user_agent})

    async def get_session(self):
        if self.session is None:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))
        return self.session

    async def fetch(self, url):
        session = await self.get_session()
        try:
            async with session.get(url, timeout=30) as response:
                return await response.text()
        except Exception as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            raise

    async def close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    async def __aenter__(self):
        await self.get_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session()
