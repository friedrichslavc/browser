from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QToolTip
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtGui import QIcon, QFont
import os
import logging

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
        layout = QVBoxLayout(central_widget)

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

        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.refresh_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.go_button)

        layout.addLayout(nav_layout)

        self.web_view = QWebEngineView()
        self.web_view.setPage(CustomWebEnginePage(self.web_view))
        layout.addWidget(self.web_view)

        # Connect signals
        self.back_button.clicked.connect(self.web_view.back)
        self.forward_button.clicked.connect(self.web_view.forward)
        self.refresh_button.clicked.connect(self.web_view.reload)
        self.go_button.clicked.connect(self.navigate)
        self.url_bar.returnPressed.connect(self.navigate)

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
        self.web_view.setUrl(QUrl(url))
        logging.info(f"Navigating to: {url}")

    def display_content(self, content):
        self.web_view.setHtml(content)
        logging.info("Displaying custom content")

    def run(self):
        self.show()
        logging.info("Browser GUI started")
