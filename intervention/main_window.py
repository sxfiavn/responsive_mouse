import tkinter as tk
import threading
import random
import time
from collections import deque
from intervention.screens.intro_screen import IntroScreen
from intervention.screens.breathing_ui import BreathingScreen
from intervention.screens.grounding_ui import GroundingScreen
from assets.create_assets import load_image, TEXT_COLOR, PRIMARY_BG, BUTTON_FONT
from intervention.sensor_loop import start_sensor_loop
from intervention.monitor_stress import start_monitoring

# Description:
# Role: Central UI controller

# Responsibility:
# Hosts the name entry screen
# Transitions to the main screen after name input
# Triggers the sensor and monitoring threads
# Provides a .show_screen() method to swap UI screens

# Talks to:
# sensor_loop.py (sensor input)
# realtime_stress_detection.py (model prediction)
# screens/*.py (UI views)

class MainApp(tk.Tk):
    def __init__(self, participant_id="anon", trial="default", session_path="experiment_data/temp"):
        super().__init__()

        self.participant_id = participant_id
        self.trial = trial
        self.session_path = session_path

        self.title("Stress Intervention")
        self.geometry("600x230")
        self.configure(bg="#96C494")
        self.resizable(False, False)
        self.buffer = deque(maxlen=500)  # 10s @ 50Hz

        self.name = tk.StringVar()
        self.container = tk.Frame(self, bg="#96C494")
        self.container.pack(fill="both", expand=True)

        self.curr_command = random.choice([self.go_to_breathing, self.go_to_grounding])

        # Show IntroScreen INSIDE container
        intro = IntroScreen(self.container, self)
        intro.pack(fill="both", expand=True)

        # Flag to check if monitoring is active
        self.sensor_thread_started = False

        self.last_intervention_time = 0


    def background_activity(self, name, text):

        for widget in self.container.winfo_children():
            widget.destroy()
        
        self.name.set(name) # Set the name variable

        # make window big enough to only show the message
        self.geometry("600x230")

        # Create the main screen UI
        welcoming = text + " " + name + "!"
        label = tk.Label(self.container, text=welcoming, font=("Quicksand", 16), fg="white", bg="#96C494")
        label.pack(pady=10)

        # Add message: "We'll let you know when it's time to take a break"
        message = tk.Label(self.container, text="We'll let you know when it's time to take a break", font=("Quicksand", 14), fg="white", bg="#96C494")
        message.pack(pady=10)

        # Add message: "You got this!"
        message = tk.Label(self.container, text="You got this!", font=("Quicksand", 20), fg="white", bg="#96C494")
        message.pack(pady=10)

        # Add a button to start the breathing exercise
        start_btn = tk.Button(
            self.container,
            text="Help me calm down",
            command=self.show_ready_message,
            font=("Quicksand", 14),
            fg="black",          # White text
            bg="#96C494",       # Green background
            activebackground="#96C494",  # Same green for active state
            bd=0,                # No border
            pady=0,
            padx=0,
            relief="flat"        # Flat button for modern look
        )
        start_btn.pack(pady=20)
        

        # Thread and sensor initialization

        self.buffer.clear()
        
        # Only start the sensor thread once
        if not self.sensor_thread_started:
            threading.Thread(
                target=start_sensor_loop,
                args=(self.buffer,),
                daemon=True
            ).start()
            self.sensor_thread_started = True

        # Always reset the monitoring flag
        self.monitoring_active = True

        # Start a new thread every time background_activity is called
        threading.Thread(
            target=start_monitoring,
            args=(
                self.buffer,
                self,
                self.show_ready_message,
                lambda: self.monitoring_active
                #,lambda: self.can_trigger_intervention()
            ),
            daemon=True
        ).start()



    def show_ready_message(self):
        self.monitoring_active = False

        for widget in self.container.winfo_children():
            widget.destroy()

        name = self.name.get()
        msg = f"{name}, you will feel better after this relaxation exercise.\nAre you ready to start?"
        label = tk.Label(self.container, text=msg, font=("Quicksand", 14), fg="white", bg="#96C494", wraplength=400, justify="center")
        label.pack(pady=10)

        btn_frame = tk.Frame(self.container, bg="#96C494")
        btn_frame.pack(pady=0, expand=False)

        im_ready_img = load_image("assets/im_ready_button_g.png", size=(350, 100))
        im_ready_btn = tk.Button(
            btn_frame,
            image=im_ready_img,
            command=self.on_user_confirmed_ready,
            borderwidth=0,
            highlightthickness=0,
            bg="#96C494",
            activebackground="#96C494",
            relief="flat"
        )
        #im_ready_btn.image = im_ready_img
        im_ready_btn.pack()


        im_not_ready_btn = tk.Button(
            btn_frame,
            text="I'm not ready yet",
            command=lambda: self.background_activity(self.name.get(), "Welcome Back, "),
            font=("Quicksand", 12),
            bg="#96C494",
            fg="black"
        )
        im_not_ready_btn.pack(pady=5)


    def on_user_confirmed_ready(self):
        # Update the timestamp
        self.last_intervention_time = time.time()

        # Call whatever the next screen is
        self.curr_command()

    def go_to_breathing(self):

        # Stop the monitoring thread
        self.monitoring_active = False

        # Update next command to go to grounding
        self.curr_command = self.go_to_grounding
 
        # Destroy all widgets in the container
        for widget in self.container.winfo_children():
            widget.destroy()
        # Replace root window content with BreathingScreen
        breathing_screen = BreathingScreen(self.container, self)
        breathing_screen.pack(fill="both", expand=True)

    def go_to_grounding(self):
        # Stop the monitoring thread
        self.monitoring_active = False

        # Update next command to go to breathing
        self.curr_command = self.go_to_breathing

        # Destroy all widgets in the container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Replace root window content with GroundingScreen
        grounding_screen = GroundingScreen(self.container, self)
        grounding_screen.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
