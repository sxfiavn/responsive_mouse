import tkinter as tk
from intervention.screens.breathing_ui import BreathingScreen

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stress Intervention")
        self.geometry("600x400")
        self.configure(bg="#524A8F")
        self.resizable(False, False)

        self.name = tk.StringVar()
        self.container = tk.Frame(self, bg="#524A8F")
        self.container.pack(fill="both", expand=True)

        self.show_name_prompt()

    def show_name_prompt(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        label = tk.Label(self.container, text="What is your name?", font=("Quicksand", 14), fg="white", bg="#524A8F")
        label.pack(pady=20)

        entry = tk.Entry(self.container, textvariable=self.name, font=("Quicksand", 14))
        entry.pack()

        submit_btn = tk.Button(self.container, text="Submit", command=self.show_ready_message, font=("Quicksand", 12))
        submit_btn.pack(pady=10)

    def show_ready_message(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        name = self.name.get() or "Friend"
        msg = f"{name}, you will feel better after this relaxation exercise.\nAre you ready to start?"

        label = tk.Label(self.container, text=msg, font=("Quicksand", 14), fg="white", bg="#524A8F", wraplength=400, justify="center")
        label.pack(pady=40)

        yes_btn = tk.Button(self.container, text="Yes", font=("Quicksand", 12), command=self.go_to_breathing)
        yes_btn.pack(pady=5)

        no_btn = tk.Button(self.container, text="No", font=("Quicksand", 12), command=self.quit)
        no_btn.pack(pady=5)

    def go_to_breathing(self):
        self.container.destroy()  # Remove intro UI

        # Replace root window content with BreathingScreen
        breathing_screen = BreathingScreen(self)
        breathing_screen.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
