# DNS解析框架
import socket

class DNSResolver:
    def __init__(self):
        self.cache = {}

    def resolve(self, domain):
        if domain in self.cache:
            return self.cache[domain]
        
        try:
            ip = socket.gethostbyname(domain)
            self.cache[domain] = ip
            return ip
        except socket.gaierror:
            return None
