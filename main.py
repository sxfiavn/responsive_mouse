# Role: Entry point for the app
# Responsibility: Launches the Tkinter interface (MainApp from main_window.py)

# Run this script to start the application
from intervention.main_window import MainApp

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
