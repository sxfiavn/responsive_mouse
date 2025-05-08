import uuid
import os
import subprocess
import time
from datetime import datetime
import serial

def get_participant_metadata():
    # Prompt for participant ID and trial label
    print("Welcome to the Experiment Setup!")
    pid = input("Enter Participant ID (or leave blank to auto-generate): ").strip()
    if not pid:
        pid = f"PID_{uuid.uuid4().hex[:6]}"
        print(f"Generated Participant ID: {pid}")

    trial = input("Enter Trial Label (e.g., 'baseline', 'intervention1'): ").strip()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create folder
    session_path = f"experiment_data/{pid}/{trial}_{timestamp}"
    os.makedirs(session_path, exist_ok=True)

    return pid, trial, session_path

def log_event(session_path, message):
    with open(os.path.join(session_path, "events.log"), "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")

def baseline_check(pid, session_path):
    # print in terminal and ask for researcher to confirm they want to start baseline check with input
    print("Please confirm you want to start the baseline check (y/n): ", end="")
    while True:
        confirm = input().strip().lower()
        if confirm in ['y', 'yes']:
            break
        elif confirm in ['n', 'no']:
            print("Baseline check cancelled.")
            return
        else:
            print("Invalid input. Please enter 'y' or 'n': ", end="")

    print("Starting baseline check...")
    print("Please ensure the participant is in a comfortable position and not moving.")
    print("Baseline check will last for 60 seconds.")
    print("You can start the baseline check now.")
    print("You have 10 seconds to prepare. Press Enter to start the countdown.")
    input()  # Wait for the researcher to press Enter
    for i in range(10, 0, -1):
        print(f"Starting in {i} seconds...", end="\r")
        time.sleep(1)
    print("\nBaseline check started. Please wait...")
    
    # Start reading from serial
    port = "/dev/cu.usbmodem744DBD9FD0942"  # ← adjust your actual port
    ser = serial.Serial(port, 115200)

    log_path = os.path.join(session_path, "baseline_data.csv")
    with open(log_path, "w") as f:
        f.write("timestamp,ppg,gsr\n")
        start = time.time()
        while time.time() - start < 60:
            try:
                line = ser.readline().decode().strip()
                ppg, gsr = map(int, line.split(","))
                f.write(f"{time.time()},{ppg},{gsr}\n")
            except Exception:
                continue
    
    print("Baseline check complete.")


def run_ui_session(session_path, pid, trial):
    # Run the UI session
    # are you ready to start the UI session? (y/n)
    print(f"Are you ready to start the {trial} session? (y/n): ", end="")
    while True:
        confirm = input().strip().lower()
        if confirm in ['y', 'yes']:
            break
        elif confirm in ['n', 'no']:
            print("UI session cancelled.")
            return
        else:
            print("Invalid input. Please enter 'y' or 'n': ", end="")
    print("Starting UI session...")
    subprocess.run(["python", "main.py", pid, trial, session_path])
    log_event(session_path, f"Ended session: {trial}")

def running_experiment():
    pid, trial, session_path = get_participant_metadata()
    log_event(session_path, f"Participant ID: {pid}, Trial: {trial}, Session Path: {session_path}")
    if trial == "baseline":
        baseline_check(pid, session_path)
        log_event(session_path, "Baseline check completed.")
    else:
        run_ui_session(session_path, pid, trial)
        log_event(session_path, f"Ended session: {trial}")

if __name__ == "__main__":
    running_experiment()
# This script is designed to run the experiment setup, including participant metadata collection,
# baseline check, and UI session. It logs events to a file and handles user input for confirmation.

# Setting up the experiment:
# 1. Open new terminal
# 2. Paste (without quotations): "cd Desktop/responsive_mouse"

# Baseline:
# 1. run the script: "python experimental_setup/run_experiment.py"
# 2. leave participant id blank -> store the response in a sticky note
# 3. for trial input (without the quotations): "baseline"
# 4. Press "y" and Enter to confirm the baseline check 
# 5. once the participant is ready, press Enter to start the countdown for baseline check (10 seconds)
# 6. wait for the script to finish

# Intervention (for both intervention1 and intervention2):
# 1. run the script: "python experimental_setup/run_experiment.py"
# 2. paste the participant id we stored in the sticky note
# 3. for trial input (without the quotations): "intervention1"
# 4. Press "y" and Enter to confirm the intervention check
# 5. Intervention screen will open, let participant interact with it
# 6. Once done, close the "Stress Intervention" window
