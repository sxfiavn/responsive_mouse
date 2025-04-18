# log_data.py
import csv
import serial
import time
import os
from config import SERIAL_PORT, BAUD_RATE, LABEL, DURATION

# ——— Prompt the user for participant ID, label, and trial ——— #
participant_id = input("Enter Participant ID: ")
label = input("Enter the Label (e.g., 'resting', 'stressed'): ")
trial = input("Enter the Trial Number/Name (e.g., 'trial1', 'trial2'): ")

# Generate the filename using the inputs and trial time
filename = f"../data/{participant_id}_{label}_{trial}.csv"

# ---- Serial Port Setup ——— #
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

start_time = time.time()

with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestep', 'ppg_raw', 'gsr_raw', 'label'])

    try:
        while True:
            line = ser.readline().decode().strip()
            if "," in line:
                timestep = round(time.time() - start_time, 2)
                ppg_raw, gsr_raw = map(int, line.split(","))

                writer.writerow([timestep, ppg_raw, ppg_smooth, gsr_raw, gsr_smooth, LABEL])
                print(f"{timestep} | PPG: {ppg_raw} | GSR: {gsr_raw}")

                if DURATION and time.time() - start_time > DURATION:
                    break
        
        print("Saving to:", os.path.abspath(filename))

    except KeyboardInterrupt:
        print("Logging stopped.")
    finally:
        ser.close()
