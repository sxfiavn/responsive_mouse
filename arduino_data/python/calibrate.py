import serial
import time
import csv
import os
from config import SERIAL_PORT, BAUD_RATE

# ---- Serial Port Setup ---- #
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)  # Allow time for Arduino to reset

# ---- Settings ---- #
num_samples = 100
filename_csv = "calibration_data.csv"
filename_txt = "calibration_data.txt"

def collect_samples(phase_name):
    print(f"\nStarting {phase_name} calibration...")
    print(f"Collecting {num_samples} samples...")
    
    ppg_total = 0
    gsr_total = 0
    ppg_values = []
    gsr_values = []

    for i in range(num_samples):
        line = ser.readline().decode().strip()
        if "," in line:
            try:
                ppg_raw, gsr_raw = map(int, line.split(","))
                ppg_total += ppg_raw
                gsr_total += gsr_raw
                ppg_values.append(ppg_raw)
                gsr_values.append(gsr_raw)

                with open(filename_csv, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([phase_name, i + 1, ppg_raw, gsr_raw])

            except ValueError:
                continue  # skip malformed line

    ppg_avg = ppg_total / num_samples
    gsr_avg = gsr_total / num_samples

    print(f"{phase_name} Calibration Complete!")
    print(f"PPG: {ppg_avg:.2f}, GSR: {gsr_avg:.2f}")

    return ppg_avg, gsr_avg


# ---- Setup Files ---- #
# Create or clear CSV file
with open(filename_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Phase", "Sample", "PPG_Raw", "GSR_Raw"])

# ---- Phase 1: Hands OFF ---- #
print("PHASE 1: Please remove your hand from the mouse/sensors.")
input("Press Enter when ready to start hands-off calibration...")
ppg_off, gsr_off = collect_samples("Hands_Off")

# ---- Phase 2: Hands ON ---- #
print("\nPHASE 2: Place your hand naturally on the mouse/sensors.")
input("Press Enter when ready to start hands-on calibration...")
ppg_on, gsr_on = collect_samples("Hands_On")

# ---- Save Baseline Summary ---- #
with open(filename_txt, 'w') as f:
    f.write("Sensor Calibration Results:\n")
    f.write(f"PPG (hands off): {ppg_off:.2f}\n")
    f.write(f"PPG (resting hand on): {ppg_on:.2f}\n")
    f.write(f"GSR (hands off): {gsr_off:.2f}\n")
    f.write(f"GSR (resting hand on): {gsr_on:.2f}\n")

print(f"\n✅ Calibration complete. Data saved to:\n- {filename_csv}\n- {filename_txt}")
ser.close()
