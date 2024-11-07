import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QProgressBar
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))

        # Create a progress bar
        self.loading_bar = QProgressBar()
        self.loading_bar.setValue(0)
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Create navigation buttons
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)

        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.go_forward)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_page)

        self.home_button = QPushButton("Home") 
        self.home_button.clicked.connect(self.go_home) # Take action upon clicking the button

        # Layout for the navigation bar
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.refresh_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.home_button)

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(nav_layout)
        self.layout.addWidget(self.loading_bar) # Used to see the loading state of a website
        self.layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.setWindowTitle("WebMD Project - Browser")  # Set the window title
        self.resize(1000, 700)  # Set the window size

        # Connect signals for loading progress
        self.browser.loadStarted.connect(self.on_load_started)
        self.browser.loadFinished.connect(self.on_load_finished)

        self.show()

    def navigate_to_url(self): # Open website on startup
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def refresh_page(self):
        self.browser.reload()  # Reload the current page

    def go_back(self):
        self.browser.back()  # Go back in history

    def go_forward(self):
        self.browser.forward()  # Go forward in history

    def go_home(self):
        url = "http://google.com" # Desired home page
        self.browser.setUrl(QUrl(url)) # Going to the home page

    def progress_bar(self):
        def on_load_started(self):
            self.loading_bar.setValue(0) # Reset loading bar
            self.loading_bar.setMaximum(0) # Indeterminate mode (?)

        def on_load_finished(self, success):
            self.loading_bar.setMaximum(1) # Set maximum to 1 for completion
            self.loading_bar.setValue(1) # Set loading bar to complete
            if success:
                self.url_bar.setText(self.browser.url().toString()) # Update URL bar with current URL
            else:
                print("Failed to load page.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    sys.exit(app.exec())
