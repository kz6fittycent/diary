package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	// Create a new Fyne application
	myApp := app.New()
	myWindow := myApp.NewWindow("Diary")

	// Placeholder for username and password input
	username := widget.NewEntry()
	username.SetPlaceHolder("Enter your username")

	password := widget.NewPasswordEntry()
	password.SetPlaceHolder("Enter your password")

	// URL entry
	url := widget.NewEntry()
	url.SetPlaceHolder("Enter your Nextcloud URL (e.g., https://example.com)")

	// Login button
	loginButton := widget.NewButton("Login", func() {
		// Logic for handling login can go here
		// For now, we'll just print the credentials
		println("Username:", username.Text)
		println("Password:", password.Text)
		println("URL:", url.Text)
	})

	// Create the main content
	content := container.NewVBox(
		widget.NewLabel("Welcome to Diary"),
		username,
		password,
		url,
		loginButton,
	)

	// Set the content and show the window
	myWindow.SetContent(content)
	myWindow.Resize(fyne.NewSize(400, 300))
	myWindow.ShowAndRun()
}
