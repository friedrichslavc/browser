# 简单的HTML解析框架
from bs4 import BeautifulSoup
import re

class HTMLParser:
    def parse(self, html_content):
        return BeautifulSoup(html_content, 'html.parser')

    def get_title(self, soup):
        return soup.title.string if soup.title else "No title"

    def get_links(self, soup):
        return [link.get('href') for link in soup.find_all('a') if link.get('href')]

    def get_text(self, soup):
        return ' '.join(soup.stripped_strings)

    def get_meta_tags(self, soup):
        return {tag.get('name', tag.get('property')): tag.get('content') for tag in soup.find_all('meta') if tag.get('name') or tag.get('property')}

    def get_images(self, soup):
        return [img.get('src') for img in soup.find_all('img') if img.get('src')]

    def sanitize_html(self, html_content):
        # 简单的HTML净化，移除潜在的危险标签和属性
        soup = BeautifulSoup(html_content, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        return str(soup)
