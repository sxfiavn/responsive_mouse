import tkinter as tk
from assets.create_assets import load_image

class BreathingScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#524A8F")
        self.controller = controller  # this is MainApp

        # resize window
        controller.geometry("1400x800") 

        # Create a label for the welcome message
        self.welcome_label = tk.Label(self, text="Welcome to the Breathing Exercise", font=("Quicksand", 20), bg="#524A8F", fg="white")
        self.welcome_label.pack(pady=20)

        # Create a label for the instructions
        self.instructions_label = tk.Label(self, text="We'll start with some breathing exercises. Just follow the instructions on the screen", font=("Quicksand", 16), bg="#524A8F", fg="white")
        self.instructions_label.pack(pady=30)

        # Create a button to start the exercise
        # note: currently uses text, not image
        self.im_ready_img = load_image("assets/im_ready_button_p.png", size=(350, 100))
        self.im_ready_btn = tk.Button(
            self,  
            image=self.im_ready_img,
            command=self.start_breathing_exercise,
            borderwidth=0,
            highlightthickness=0,
            bg="#96C494",
            activebackground="#96C494",
            relief="flat"
        )
        #self.im_ready_btn.image = im_ready_img
        self.im_ready_btn.pack()

    def start_breathing_exercise(self):
        # Destroy the welcome label and button
        self.welcome_label.destroy()
        self.im_ready_btn.destroy()
        self.instructions_label.destroy()

        # Instruction text
        self.header = tk.Label(self, text="Let’s take some deep breaths.",
                               font=("Quicksand", 20), bg="#524A8F", fg="white")
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

        # Start the breathing exercise
        self.breath_label.config(text="We'll start in 5 seconds...")
        self.after(5000, self.run_breathing_cycle)

    def run_breathing_cycle(self):

        if self.cycle_count >= self.max_cycles:

            # Stop the breathing exercise
            self.canvas.destroy()  # Remove the canvas
            self.header.config(text="Breathing exercise complete.")
            self.breath_label.config(text="How do you feel?")

            # TODO: fix button UI
            # Button to "I'm ready to go back to my work"
            go_back_btn = tk.Button(self, text="I'm ready to go back to my work", command=self.go_back,
                                   font=("Quicksand", 12), bg="#524A8F", fg="black")
            go_back_btn.pack(pady=5)   

            # TODO: fix button UI
            # Button to "I want to do another exercise"
            another_exercise_btn = tk.Button(self, text="I want to do another exercise", command=self.controller.go_to_grounding,
                                   font=("Quicksand", 12), bg="#524A8F", fg="black")
            another_exercise_btn.pack(pady=5)
            return
        
        elif self.state == "in":
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
        delay = 80
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

    def go_back(self):
        # go back to main screen to
        name = self.controller.name.get()
        self.controller.background_activity(name, f"Welcome Back, ")
        self.destroy()


if __name__ == "__main__":
    app = BreathingScreen()
    app.mainloop()
