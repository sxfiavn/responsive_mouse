import tkinter as tk

class IntroScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#96C494")
        self.controller = controller  # this is MainApp

        # Create a Var to hold the name
        self.parent = parent
        self.name = tk.StringVar()

    
        # Instruction text
        label = tk.Label(self, text="Hi There! What is your name?", font=("Quicksand_bold", 20), fg="white", bg="#96C494")
        label.pack(pady=20)

        entry = tk.Entry(self, textvariable=self.name, font=("Quicksand", 14))
        entry.pack()

        # TODO: Change button UI
        submit_btn = tk.Button(self, text="Continue", command=self.go_to_main_screen, font=("Quicksand", 12), fg="black")
        submit_btn.pack(pady=10)

    
    def go_to_main_screen(self):
        # Get the name from the entry field
        name = self.name.get()
        if not name:
            name = "Friend"
        self.name.set(name)

        # Go to main window UI
        self.controller.background_activity(name, "Hello,")
        self.destroy()


if __name__ == "__main__":
    app = IntroScreen()
    app.mainloop()
