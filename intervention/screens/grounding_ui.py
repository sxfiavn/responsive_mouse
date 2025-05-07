import tkinter as tk
from assets.create_assets import load_image
class GroundingScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#524A8F")
        self.controller = controller  # this is MainApp
        self.current_step = 0

        # resize window - fullscreen
        controller.geometry("1400x800") 

        # Load images and instructions
        self.instructions_text = [
            "Name 5 things you can see.",
            "Name 4 things you can touch.",
            "Name 3 things you can hear.",
            "Name 2 things you can smell.",
            "Name 1 thing you can taste."
        ]

        self.image_list = [
            load_image("assets/eye.png", size=(300, 300)),
            load_image("assets/hand.png", size=(300, 300)),
            load_image("assets/ear.png", size=(300, 300)),
            load_image("assets/nose.png", size=(300, 300)),
            load_image("assets/mouth.png", size=(300, 300))
        ]

        # Create a label for the welcome message
        welcome_label = tk.Label(self, text="Welcome to the Grounding Exercise", font=("Quicksand", 20), bg="#524A8F", fg="white")
        welcome_label.pack(pady=20)

        # Create a label for the instructions
        self.instructions_label = tk.Label(self, text="We'll start with some grounding exercises. Just follow the instructions on the screen", font=("Quicksand", 16), bg="#524A8F", fg="white")
        self.instructions_label.pack(pady=10)

        # Create a button to start the exercise
        # note: currently uses text, not image
        self.im_ready_img = load_image("assets/im_ready_button1.png", size=(350, 100))
        self.im_ready_btn = tk.Button(
            self,  
            text="Start!",
            command=self.go_to_next_section,
            borderwidth=0,
            highlightthickness=0,
            bg="#96C494",
            activebackground="#96C494",
            relief="flat"
        )
        #self.im_ready_btn.image = im_ready_img
        self.im_ready_btn.pack()

        # Not packed yet
        self.image_label = tk.Label(self, bg="#524A8F")

        # "Next" button to go through steps
        next_exercise_img = load_image("assets/excercise_btn.png", size=(250, 60))
        self.next_button = tk.Button(
            self,
            image=next_exercise_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.go_to_next_section,
            font=("Quicksand", 14),
            bg="#96C494",
            fg="black",
            relief="flat"
        )

    def go_to_next_section(self):
        self.im_ready_btn.destroy()

        if self.current_step == 0:
            # First time only: show labels and next button
            self.image_label.pack(pady=20)
            self.next_button.pack(pady=30)

        if self.current_step >= len(self.instructions_text):
            self.next_button.destroy()
            self.instructions_label.config(text="All done! How do you feel?")
            self.image_label.pack_forget()
            go_back_btn = tk.Button(self, text="I'm ready to go back to my work", command=self.go_back,
                                   font=("Quicksand", 12), bg="#524A8F", fg="black")
            go_back_btn.pack(pady=5)   

            another_exercise_btn = tk.Button(self, text="I want to do another exercise", command=self.controller.go_to_grounding,
                                   font=("Quicksand", 12), bg="#524A8F", fg="black")
            another_exercise_btn.pack(pady=5)
            return

        self.instructions_label.config(text=self.instructions_text[self.current_step])
        self.image_label.config(image=self.image_list[self.current_step])
        self.image_label.image = self.image_list[self.current_step]  # prevent garbage collection

        self.current_step += 1
            

    def go_back(self):
        # go back to main screen to
        name = self.controller.name.get()
        self.controller.background_activity(name, f"Welcome Back, ")
        self.destroy()

if __name__ == "__main__":
    app = GroundingScreen()
    app.mainloop()
