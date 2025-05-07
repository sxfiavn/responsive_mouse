# main.py
import sys
from intervention.main_window import MainApp

if __name__ == "__main__":
    # Default values if not provided
    pid = "anon"
    trial = "default"
    session_path = "experiment_data/temp"

    if len(sys.argv) >= 4:
        pid = sys.argv[1]
        trial = sys.argv[2]
        session_path = sys.argv[3]

    app = MainApp(participant_id=pid, trial=trial, session_path=session_path)
    app.mainloop()
