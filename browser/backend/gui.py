import importlib
import sys
import os
import subprocess
import logging
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QToolTip, QInputDialog, QMessageBox, QSplitter, QListWidget, QListWidgetItem
from PyQt5.QtCore import QUrl, pyqtSlot, Qt, QTimer
from PyQt5.QtGui import QIcon, QFont
QtWebEngineWidgets = importlib.import_module('PyQt5.QtWebEngineWidgets')
QWebEngineView = QtWebEngineWidgets.QWebEngineView
QWebEnginePage = QtWebEngineWidgets.QWebEnginePage


# 设置日志
logging.basicConfig(filename='browser.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        log_message = f"JS: {message} (line {lineNumber}, source: {sourceID})"
        logging.info(log_message)

class BrowserGUI(QMainWindow):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Simple Browser')
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowIcon(QIcon('path/to/your/icon.png'))  # Add your browser icon here

        # Set up tooltips
        QToolTip.setFont(QFont('SansSerif', 10))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Navigation toolbar
        nav_layout = QHBoxLayout()
        self.back_button = QPushButton('←')
        self.back_button.setToolTip('Go back')
        self.forward_button = QPushButton('→')
        self.forward_button.setToolTip('Go forward')
        self.refresh_button = QPushButton('↻')
        self.refresh_button.setToolTip('Refresh page')
        self.url_bar = QLineEdit()
        self.go_button = QPushButton('Go')
        self.go_button.setToolTip('Navigate to URL')
        
        self.bookmark_button = QPushButton('☆')
        self.bookmark_button.setToolTip('Bookmarks')
        self.history_button = QPushButton('⌛')
        self.history_button.setToolTip('History')

        self.add_bookmark_button = QPushButton('+☆')
        self.add_bookmark_button.setToolTip('Add Bookmark')

        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.refresh_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.go_button)
        nav_layout.addWidget(self.bookmark_button)
        nav_layout.addWidget(self.history_button)
        nav_layout.addWidget(self.add_bookmark_button)

        main_layout.addLayout(nav_layout)

        # Create a splitter for the main content and sidebar
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)

        # Create the main web view
        self.web_view = QWebEngineView()
        self.web_view.setPage(CustomWebEnginePage(self.web_view))
        self.splitter.addWidget(self.web_view)

        # Create the sidebar for bookmarks and history
        self.sidebar = QListWidget()
        self.sidebar.setVisible(False)  # Initially hidden
        self.splitter.addWidget(self.sidebar)

        # Set the initial sizes of the splitter
        self.splitter.setSizes([800, 200])  # Adjust these values as needed

        # Connect signals
        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)
        self.refresh_button.clicked.connect(self.web_view.reload)
        self.go_button.clicked.connect(self.navigate)
        self.url_bar.returnPressed.connect(self.navigate)
        self.bookmark_button.clicked.connect(self.toggle_bookmarks)
        self.history_button.clicked.connect(self.show_history)
        self.add_bookmark_button.clicked.connect(self.add_bookmark)
        self.sidebar.itemClicked.connect(self.sidebar_item_clicked)

        # Load the initial HTML file
        initial_url = QUrl.fromLocalFile(os.path.abspath('frontend/browser_ui.html'))
        self.web_view.setUrl(initial_url)

        # Connect web view signals
        self.web_view.loadFinished.connect(self.onLoadFinished)
        self.web_view.urlChanged.connect(self.onUrlChanged)

        logging.info("Browser GUI initialized")

    def onLoadFinished(self, ok):
        if ok:
            self.web_view.page().runJavaScript("""
                window.pywebview = {
                    api: {
                        navigate: function(url) {
                            window.location.href = url;
                        }
                    }
                };
            """)
            logging.info(f"Page loaded successfully: {self.web_view.url().toString()}")
        else:
            logging.error(f"Failed to load page: {self.web_view.url().toString()}")

    def onUrlChanged(self, url):
        self.url_bar.setText(url.toString())
        logging.info(f"URL changed to: {url.toString()}")

    @pyqtSlot()
    def navigate(self):
        url = self.url_bar.text()
        if not url.startswith('http'):
            url = 'http://' + url
        asyncio.ensure_future(self.browser.navigate(url))
        logging.info(f"Navigating to: {url}")

    def display_content(self, content):
        self.web_view.setHtml(content)
        logging.info("Displaying custom content")

    async def display_error(self, message):
        self.web_view.setHtml(f"<h1>Error</h1><p>{message}</p>")
        logging.error(f"Displaying error: {message}")

    async def navigate_async(self, url):
        content = await self.browser.navigate(url)
        self.display_content(content)

    async def run(self):
        self.show()
        logging.info("Browser GUI started")

    def toggle_bookmarks(self):
        if self.sidebar.isVisible() and self.sidebar.property("current_view") == "bookmarks":
            self.sidebar.setVisible(False)
        else:
            self.show_bookmarks()

    def show_bookmarks(self):
        self.sidebar.clear()
        bookmarks = self.browser.get_bookmarks()
        for title, url in bookmarks:
            item = QListWidgetItem(f"{title} ({url})")
            item.setData(Qt.UserRole, url)
            self.sidebar.addItem(item)
        self.sidebar.setProperty("current_view", "bookmarks")
        self.sidebar.setVisible(True)
        logging.info("Showing bookmarks in sidebar")

    def show_history(self):
        history = self.browser.get_history()
        logging.info(f"Showing history. Current history: {history}")
        history_html = "<h1>History (Last 10 Visits)</h1><ul>"
        if history:
            for url, title in history:
                display_title = title if title else url
                history_html += f"<li><a href='{url}'>{display_title}</a></li>"
        else:
            history_html += "<li>No history yet</li>"
        history_html += "</ul>"
        self.sidebar.clear()
        for url, title in history:
            display_title = title if title else url
            item = QListWidgetItem(f"{display_title} ({url})")
            item.setData(Qt.UserRole, url)
            self.sidebar.addItem(item)
        self.sidebar.setProperty("current_view", "history")
        self.sidebar.setVisible(True)

    def add_bookmark(self):
        title, ok = QInputDialog.getText(self, 'Add Bookmark', 'Enter bookmark title:')
        if ok and title:
            url = self.web_view.url().toString()
            self.browser.add_bookmark(title, url)
            QMessageBox.information(self, 'Bookmark Added', f'Bookmark "{title}" has been added.')
            logging.info(f"GUI: Added bookmark {title} - {url}")
            if self.sidebar.property("current_view") == "bookmarks":
                self.show_bookmarks()  # Refresh the bookmarks view

    def sidebar_item_clicked(self, item):
        url = item.data(Qt.UserRole)
        self.web_view.setUrl(QUrl(url))

    @pyqtSlot()
    def go_back(self):
        asyncio.ensure_future(self.browser.go_back())

    @pyqtSlot()
    def go_forward(self):
        asyncio.ensure_future(self.browser.go_forward())

    def closeEvent(self, event):
        logging.info("Browser GUI is closing")
        self.schedule_log_cleanup()
        event.ignore()  # 阻止窗口立即关闭

    def schedule_log_cleanup(self):
        script_path = os.path.join(os.path.dirname(__file__), 'cleanup_logs.py')
        cleanup_process = subprocess.Popen([sys.executable, script_path], 
                                           stdout=subprocess.PIPE, 
                                           stderr=subprocess.PIPE, 
                                           universal_newlines=True)
        
        # 创建一个定时器来检查清理进程的输出
        self.cleanup_timer = QTimer()
        self.cleanup_timer.timeout.connect(lambda: self.check_cleanup_status(cleanup_process))
        self.cleanup_timer.start(1000)  # 每秒检查一次

    def check_cleanup_status(self, process):
        output = process.stdout.readline().strip()
        if output == "CLEANUP_COMPLETE":
            self.cleanup_timer.stop()
            QApplication.instance().quit()  # 关闭整个应用
        elif process.poll() is not None:
            self.cleanup_timer.stop()
            print("Cleanup process ended unexpectedly")
