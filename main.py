import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QProgressBar, QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))
        self.layout.addWidget(self.browser)

        # Create a progress bar
        self.loading_bar = QProgressBar()
        self.loading_bar.setValue(0)
        self.layout.addWidget(self.loading_bar)

        # Create a navbar
        self.navbar = QHBoxLayout()
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Create buttons for the navbar
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)

        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.go_forward)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_page)

        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.go_home)

        # Add buttons to the navigation bar
        self.navbar.addWidget(self.back_button)
        self.navbar.addWidget(self.forward_button)
        self.navbar.addWidget(self.refresh_button)
        self.navbar.addWidget(self.url_bar)
        self.navbar.addWidget(self.home_button)

        # Add the navbar to the layout
        self.layout.addLayout(self.navbar)

        # Connect signals for loading progress
        self.browser.loadStarted.connect(self.on_load_started)
        self.browser.loadFinished.connect(self.on_load_finished)
        self.browser.loadProgress.connect(self.update_load)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def refresh_page(self):
        self.browser.reload()

    def go_back(self):
        self.browser.back()

    def go_forward(self):
        self.browser.forward()

    def go_home(self):
        url = "http://google.com"
        self.browser.setUrl(QUrl(url))

    def on_load_started(self):
        self.loading_bar.setValue(0)

    def on_load_finished(self, success):
        self.loading_bar.setValue(100)
        if success:
            self.url_bar.setText(self.browser.url().toString())
        else:
            print("Failed to load page.")

    def update_load(self, progress):
        self.loading_bar.setValue(progress)

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 700)
        self.setWindowTitle("WebFG Project - Browser")

        # Create a QTabWidget
        self.tabs = QTabWidget()

        # Create a button to add new tabs
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setFixedSize(27, 27)  # Set a fixed size for the button
        self.new_tab_button.clicked.connect(self.add_new_tab)

        # Create a button to delete the current tab
        self.delete_tab_button = QPushButton("-")
        self.delete_tab_button.setFixedSize(27, 27)
        self.delete_tab_button.clicked.connect(self.delete_new_tab)

        # Create a horizontal layout for the tabs and the new tab button
        tabB_layout = QVBoxLayout()
        tabB_layout.addWidget(self.new_tab_button)  # Add the new tab button
        tabB_layout.addWidget(self.delete_tab_button) # Add the delete tab button
        tabB_layout.setContentsMargins(0, 10, 0, 0)

        # Create a section for tabs
        tab_layout = QHBoxLayout()
        tab_layout.addWidget(self.tabs)  # Add the tab widget

        # Create a main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(tab_layout)
        main_layout.addLayout(tabB_layout) # Add the tab layout to the main layout

        # Create a central widget to hold the layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Add the first tab
        self.add_new_tab()

    def add_new_tab(self):
        new_tab = BrowserTab()
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)

    def delete_new_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            self.tabs.removeTab(current_index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()  # This should be after the Browser class definition
    window.show()
    sys.exit(app.exec())
