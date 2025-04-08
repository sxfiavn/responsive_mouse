import serial
import time
import sys
import csv
from config import SERIAL_PORT, BAUD_RATE
# import matplotlib.pyplot as plt
from utils import MovingAverage

# ---- Configuration ——— #
ppg_smoother = MovingAverage(10)
gsr_smoother = MovingAverage(10)

# ---- Serial Port Setup ——— #
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)  # Allow some time for Arduino to start up

# ---- Calibration Setup ——— #
print("Starting calibration. Please ensure that the hand is off the sensors.")
input("Press Enter when ready to start calibration...")

# Collect baseline data
num_samples = 100  # Number of samples to average for calibration
ppg_baseline = 0
gsr_baseline = 0

# ---- Matplotlib Setup ——— #
# plt.ion()  # Turn on interactive mode for real-time plotting
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))  # Create two subplots
# ax1.set_title("PPG Sensor Calibration")
# ax1.set_xlabel("Samples")
# ax1.set_ylabel("PPG Value")
# ax2.set_title("GSR Sensor Calibration")
# ax2.set_xlabel("Samples")
# ax2.set_ylabel("GSR Value")

ppg_values = []
gsr_values = []
ppg_smooth_values = []
gsr_smooth_values = []

# Open CSV file to save calibration data
filename = "calibration_data.csv"
with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['Sample', 'PPG_Raw', 'PPG_Smoothed', 'GSR_Raw', 'GSR_Smoothed']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the header to the CSV

    print(f"Collecting {num_samples} samples for calibration...")

    # Collect and plot sensor data
    for i in range(num_samples):
        line = ser.readline().decode().strip()
        if "," in line:
            ppg_raw, gsr_raw = map(int, line.split(","))
            ppg_baseline += ppg_raw
            gsr_baseline += gsr_raw

            ppg_smooth = ppg_smoother.update(ppg_raw)
            gsr_smooth = gsr_smoother.update(gsr_raw)

            # Add the raw and smoothed values to the lists for plotting
            ppg_values.append(ppg_raw)
            gsr_values.append(gsr_raw)
            ppg_smooth_values.append(ppg_smooth)
            gsr_smooth_values.append(gsr_smooth)

            # Write the data to the CSV file
            writer.writerow({
                'Sample': i + 1,
                'PPG_Raw': ppg_raw,
                'PPG_Smoothed': ppg_smooth,
                'GSR_Raw': gsr_raw,
                'GSR_Smoothed': gsr_smooth
            })

            # # Plot the data in real-time
            # ax1.clear()  # Clear the previous plot
            # ax2.clear()  # Clear the previous plot
            # ax1.plot(ppg_values, label="Raw PPG", color='blue')
            # ax1.plot(ppg_smooth_values, label="Smoothed PPG", color='green')
            # ax2.plot(gsr_values, label="Raw GSR", color='red')
            # ax2.plot(gsr_smooth_values, label="Smoothed GSR", color='orange')

            # ax1.legend(loc="upper right")
            # ax2.legend(loc="upper right")

            # plt.draw()  # Redraw the plot
            # plt.pause(0.05)  # Pause for a short time to allow plot update

    # Calculate average baseline values
    ppg_baseline /= num_samples
    gsr_baseline /= num_samples

# # Final plot display
# plt.ioff()  # Turn off interactive mode
# plt.show()

print(f"Calibration Complete! Baseline values: PPG: {ppg_baseline}, GSR: {gsr_baseline}")

# Save calibration data to a file for future use
with open("calibration_data.txt", 'w') as f:
    f.write(f"PPG Baseline: {ppg_baseline}\n")
    f.write(f"GSR Baseline: {gsr_baseline}\n")

print(f"Calibration data saved to 'calibration_data.txt' and 'calibration_data.csv'. You can now use these values to adjust the sensor readings.")
ser.close()
