import json
import os
import logging

class BookmarkManager:
    def __init__(self, filename='bookmarks.json'):
        self.filename = filename
        self.bookmarks = []
        self.load_bookmarks()

    def load_bookmarks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.bookmarks = json.load(f)
            except json.JSONDecodeError:
                logging.error(f"Error decoding {self.filename}. Starting with empty bookmarks.")
        else:
            logging.info(f"Bookmark file {self.filename} not found. Creating a new one.")

    def save_bookmarks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.bookmarks, f)

    def add_bookmark(self, title, url):
        self.bookmarks.append((title, url))
        self.save_bookmarks()
        logging.info(f"Added bookmark: {title} - {url}")

    def get_bookmarks(self):
        return self.bookmarks

    def remove_bookmark(self, url):
        self.bookmarks = [b for b in self.bookmarks if b[1] != url]
        self.save_bookmarks()

    def search_bookmarks(self, query):
        return [b for b in self.bookmarks if query.lower() in b[0].lower() or query.lower() in b[1].lower()]

    def update_bookmark(self, url, new_title=None, new_url=None):
        for bookmark in self.bookmarks:
            if bookmark[1] == url:
                if new_title:
                    bookmark[0] = new_title
                if new_url:
                    bookmark[1] = new_url
                self.save_bookmarks()
                return True
        return False

    def clear_bookmarks(self):
        self.bookmarks = []
        self.save_bookmarks()

    def get_bookmark_count(self):
        return len(self.bookmarks)
