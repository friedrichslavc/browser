# 缓存机制框架
import time

class Cache:
    def __init__(self, expiration=3600):  # 默认缓存1小时
        self.cache = {}
        self.expiration = expiration

    def get(self, url):
        if url in self.cache:
            content, timestamp = self.cache[url]
            if time.time() - timestamp < self.expiration:
                return content
        return None

    def set(self, url, content):
        self.cache[url] = (content, time.time())
