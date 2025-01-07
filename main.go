package main

import (
	"fmt"
	"log"
	"net/url"

	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	myApp := app.New()
	myWindow := myApp.NewWindow("Diary")

	// Login fields
	serverEntry := widget.NewEntry()
	serverEntry.SetPlaceHolder("https://example.com")

	usernameEntry := widget.NewEntry()
	usernameEntry.SetPlaceHolder("Username")

	passwordEntry := widget.NewPasswordEntry()
	passwordEntry.SetPlaceHolder("Password")

	// Login button
	loginButton := widget.NewButton("Login", func() {
		serverURL := serverEntry.Text
		username := usernameEntry.Text
		password := passwordEntry.Text

		if err := validateURL(serverURL); err != nil {
			log.Println("Invalid server URL:", err)
			return
		}

		log.Printf("Attempting login to %s with user %s", serverURL, username)
		// TODO: Implement authentication
	})

	// Layout
	form := container.NewVBox(
		widget.NewLabel("Login to your Nextcloud Diary"),
		serverEntry,
		usernameEntry,
		passwordEntry,
		loginButton,
	)

	myWindow.SetContent(form)
	myWindow.Resize(fyne.NewSize(400, 300))
	myWindow.ShowAndRun()
}

func validateURL(rawURL string) error {
	_, err := url.ParseRequestURI(rawURL)
	return err
}
