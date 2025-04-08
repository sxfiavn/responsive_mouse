# log_data.py
import csv
import serial
import time
import sys
from datetime import datetime
from config import SERIAL_PORT, BAUD_RATE, LABEL, DURATION
from utils import MovingAverage

# ---- Configuration ——— #
ppg_smoother = MovingAverage(10)
gsr_smoother = MovingAverage(10)

# ——— Prompt the user for participant ID, label, and trial ——— #
participant_id = input("Enter Participant ID: ")
label = input("Enter the Label (e.g., 'resting', 'stressed'): ")
trial = input("Enter the Trial Number/Name (e.g., 'trial1', 'trial2'): ")

# Generate the filename using the inputs and trial time
trial_time = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"../data/{participant_id}_{label}_{trial}_{trial_time}.csv"

# ---- Serial Port Setup ——— #
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

start_time = time.time()

with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestep', 'ppg_raw', 'ppg_smooth', 'gsr_raw', 'gsr_smooth', 'label'])

    try:
        while True:
            line = ser.readline().decode().strip()
            if "," in line:
                timestep = round(time.time() - start_time, 2)
                ppg_raw, gsr_raw = map(int, line.split(","))
                ppg_smooth = ppg_smoother.update(ppg_raw)
                gsr_smooth = gsr_smoother.update(gsr_raw)

                writer.writerow([timestep, ppg_raw, ppg_smooth, gsr_raw, gsr_smooth, LABEL])
                print(f"{timestep} | PPG: {ppg_raw} → {ppg_smooth:.2f} | GSR: {gsr_raw} → {gsr_smooth:.2f}")

                if DURATION and time.time() - start_time > DURATION:
                    break

    except KeyboardInterrupt:
        print("Logging stopped.")
    finally:
        ser.close()
