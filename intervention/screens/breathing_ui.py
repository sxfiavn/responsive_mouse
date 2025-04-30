import tkinter as tk

class BreathingScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#524A8F")
        # Close button
        close_btn = tk.Button(self, text="✕", command=self.destroy,
                              bg="#524A8F", fg="white", bd=0, font=("Quicksand", 12))
        close_btn.place(x=570, y=10)

        # Instruction text
        self.header = tk.Label(self, text="Let’s take some deep breaths.",
                               font=("Quicksand", 14), bg="#524A8F", fg="white")
        self.header.pack(pady=30)

        # Breathing phase label
        self.breath_label = tk.Label(self, text="", font=("Quicksand", 18),
                                     bg="#524A8F", fg="white")
        self.breath_label.pack(pady=20)

        # Canvas for the pulsing circle
        self.canvas = tk.Canvas(self, width=300, height=300, bg="#524A8F", highlightthickness=0)
        self.canvas.pack()
        self.circle = self.canvas.create_oval(120, 120, 180, 180, fill="White", outline="")

        # Breathing cycle state
        self.state = "in"
        self.cycle_count = 0
        self.max_cycles = 4

        self.after(0, self.run_breathing_cycle)

    def run_breathing_cycle(self):
        if self.cycle_count >= self.max_cycles:
            self.breath_label.config(text="Done 🎉")
            return

        if self.state == "in":
            self.breath_label.config(text="Breathe in")
            self.animate_pulse(expanding=True)
            self.state = "out"
        else:
            self.breath_label.config(text="Breathe out")
            self.animate_pulse(expanding=False)
            self.state = "in"
            self.cycle_count += 1

        self.after(4000, self.run_breathing_cycle)

    def animate_pulse(self, expanding=True):
        # Animate the circle growing or shrinking
        start = 30 if expanding else 70
        end = 70 if expanding else 30
        steps = 20
        delay = 50
        delta = (end - start) / steps

        def step(i=0):
            if i > steps:
                return
            r = start + delta * i
            x0 = 150 - r
            y0 = 150 - r
            x1 = 150 + r
            y1 = 150 + r
            self.canvas.coords(self.circle, x0, y0, x1, y1)
            self.after(delay, step, i + 1)

        step()

if __name__ == "__main__":
    app = BreathingScreen()
    app.mainloop()
