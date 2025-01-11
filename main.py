#!/usr/bin/env python3

import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)


class DiaryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diary App")
        self.setGeometry(100, 100, 600, 400)

        # Initialize UI components
        self.initUI()

    def initUI(self):
        # Labels and input fields
        self.url_label = QLabel("Nextcloud URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("e.g., https://www.your-nextcloud-url.com")

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Your Nextcloud username")

        self.password_label = QLabel("App Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Your app-specific password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Buttons
        self.fetch_button = QPushButton("Fetch Diary Entry")
        self.fetch_button.clicked.connect(self.fetch_diary_entries)

        self.save_button = QPushButton("Save Diary Entry")
        self.save_button.clicked.connect(self.save_diary_entry)

        # Diary text field
        self.diary_input = QTextEdit()
        self.diary_input.setPlaceholderText("Diary entry content will appear here...")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.diary_input)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def fetch_diary_entries(self):
        url = self.url_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        date = "2025-01-09"  # Replace with dynamic date input if required

        if not url or not username or not password:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please ensure the server URL, username, and app-specific password are filled.",
            )
            return

        # Remove any trailing slashes from the base URL
        base_url = url.rstrip("/")

        # Construct the full API URL
        full_url = f"{base_url}/index.php/apps/diary/date/{date}"
        print(f"Debug: Fetching data from URL: {full_url}")  # Debugging

        try:
            # Make the GET request
            response = requests.get(
                full_url,
                auth=(username, password),
                headers={
                    "Accept": "application/json",
                },
                timeout=10,
            )

            print(f"Debug: Response status code: {response.status_code}")
            print(f"Debug: Response content: {response.text}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("message"):
                        self.diary_input.setPlainText(data["message"])
                        QMessageBox.information(self, "Success", "Diary entries fetched successfully!")
                    else:
                        QMessageBox.information(self, "No Data", "No entries found for the selected date.")
                except ValueError:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "The server returned an invalid JSON response.",
                    )
            elif response.status_code == 401:
                QMessageBox.warning(
                    self,
                    "Authentication Failed",
                    "Invalid username or app-specific password. Please verify your credentials.",
                )
            elif response.status_code == 404:
                QMessageBox.warning(self, "Not Found", "The Diary endpoint could not be found. Check the URL.")
            else:
                QMessageBox.warning(self, "Error", f"Unexpected response code: {response.status_code}")
        except requests.exceptions.SSLError:
            QMessageBox.critical(
                self,
                "SSL Error",
                "An SSL error occurred. Ensure the server uses a valid HTTPS certificate.",
            )
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def save_diary_entry(self):
        url = self.url_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        date = "2025-01-09"  # Replace with dynamic date input if required
        diary_content = self.diary_input.toPlainText()

        if not url or not username or not password or not diary_content:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please ensure all fields are filled, including the diary content.",
            )
            return

        # Remove any trailing slashes from the base URL
        base_url = url.rstrip("/")

        # Construct the full API URL
        full_url = f"{base_url}/index.php/apps/diary/date/{date}"
        print(f"Debug: Saving data to URL: {full_url}")  # Debugging

        try:
            # Make the PUT request
            response = requests.put(
                full_url,
                auth=(username, password),
                headers={
                    "Content-Type": "application/json",
                },
                json={"message": diary_content},
                timeout=10,
            )

            print(f"Debug: Response status code: {response.status_code}")
            print(f"Debug: Response content: {response.text}")

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Diary entry saved successfully!")
            elif response.status_code == 401:
                QMessageBox.warning(
                    self,
                    "Authentication Failed",
                    "Invalid username or app-specific password. Please verify your credentials.",
                )
            elif response.status_code == 404:
                QMessageBox.warning(self, "Not Found", "The Diary endpoint could not be found. Check the URL.")
            else:
                QMessageBox.warning(self, "Error", f"Unexpected response code: {response.status_code}")
        except requests.exceptions.SSLError:
            QMessageBox.critical(
                self,
                "SSL Error",
                "An SSL error occurred. Ensure the server uses a valid HTTPS certificate.",
            )
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiaryApp()
    window.show()
    sys.exit(app.exec_())

