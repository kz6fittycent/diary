#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
import requests

class DiaryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Diary - Nextcloud Integration")
        
        # Widgets
        self.url_label = QLabel("Nextcloud URL:")
        self.url_input = QLineEdit()
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_nextcloud)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.connect_button)
        
        self.setLayout(layout)

    def connect_to_nextcloud(self):
        url = self.url_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            response = requests.get(url, auth=(username, password), timeout=10)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Connected to Nextcloud!")
            else:
                QMessageBox.warning(self, "Error", f"Failed to connect: {response.status_code}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiaryApp()
    window.show()
    sys.exit(app.exec_())

