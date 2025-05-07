import uuid
import os
import subprocess
import time
from datetime import datetime

def get_participant_metadata():
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

def run_ui_session(session_path, pid, trial):
    log_event(session_path, f"Starting session: {trial} for {pid}")
    subprocess.run(["python", "main.py", pid, trial, session_path])
    log_event(session_path, f"Ended session: {trial}")

if __name__ == "__main__":
    pid, trial, session_path = get_participant_metadata()
    run_ui_session(session_path, pid, trial)