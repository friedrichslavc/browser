import sqlite3
from collections import deque
import logging

class HistoryManager:
    def __init__(self, db_file='history.db', max_history_size=100):
        self.db_file = db_file
        self.conn = None
        self.max_history_size = max_history_size
        self.back_stack = deque(maxlen=max_history_size)
        self.forward_stack = deque(maxlen=max_history_size)
        self.connect()
        self.load_history()

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             url TEXT NOT NULL,
             title TEXT,
             visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        ''')
        self.conn.commit()

    def load_history(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT url, title FROM history ORDER BY visit_time DESC LIMIT ?', (self.max_history_size,))
        self.back_stack = deque(cursor.fetchall(), maxlen=self.max_history_size)
        logging.info(f"Loaded history: {list(self.back_stack)}")

    def add_visit(self, url, title=""):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO history (url, title) VALUES (?, ?)', (url, title))
        self.conn.commit()
        self.back_stack.appendleft((url, title))
        self.forward_stack.clear()  # Clear forward stack on new visit
        
        # If database records exceed max_history_size, delete oldest records
        cursor.execute('DELETE FROM history WHERE id NOT IN (SELECT id FROM history ORDER BY visit_time DESC LIMIT ?)', (self.max_history_size,))
        self.conn.commit()
        logging.info(f"Added to history: {url}")

    def get_history(self):
        return list(self.back_stack)

    def clear_history(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM history')
        self.conn.commit()
        self.back_stack.clear()
        self.forward_stack.clear()

    async def add_to_history(self, url, title=""):
        self.add_visit(url, title)

    async def go_back(self):
        if len(self.back_stack) > 1:
            current = self.back_stack.popleft()
            self.forward_stack.appendleft(current)
            return self.back_stack[0][0]  # Return URL of the previous page
        return None

    async def go_forward(self):
        if self.forward_stack:
            next_page = self.forward_stack.popleft()
            self.back_stack.appendleft(next_page)
            return next_page[0]  # Return URL of the next page
        return None

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
