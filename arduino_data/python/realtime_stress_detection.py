import csv
import time
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.stats import mode
from collections import Counter

# Load trained model (ensure this path is correct) (replace this if we update model)
model = joblib.load("../model/stress_classifier.pkl")

# Get features from data (using the same method as in training)
# Might have to make window size smaller if no features are getting included
def preprocess_and_extract_features(data, window_size=250):
    """
    Extract features from the given data for classification.
    """
    # Use a sliding window approach
    overlap = 0.5
    step_size = int(window_size * (1 - overlap))

    # This should only be like 1 or 2 items long because we are only passing in 10 seconds of data
    features_list = []



    for start in range(0, len(data) - window_size + 1, step_size):
        window = data.iloc[start:start + window_size]

        # Time-domain features
        ppg_mean = window['ppg_raw'].mean()
        ppg_std = window['ppg_raw'].std()
        ppg_max = window['ppg_raw'].max()
        ppg_min = window['ppg_raw'].min()
        ppg_range = ppg_max - ppg_min
        ppg_rms = np.sqrt(np.mean(window['ppg_raw'] ** 2))
        ppg_peaks = len((window['ppg_raw'].diff() > 0).astype(int).diff().eq(-1).index)

        gsr_mean = window['gsr_raw'].mean()
        gsr_std = window['gsr_raw'].std()
        gsr_max = window['gsr_raw'].max()
        gsr_min = window['gsr_raw'].min()
        gsr_range = gsr_max - gsr_min
        gsr_rms = np.sqrt(np.mean(window['gsr_raw'] ** 2))
        gsr_peaks = len((window['gsr_raw'].diff() > 0).astype(int).diff().eq(-1).index)

        # GSR-specific features
        gsr_amplitude = gsr_max - gsr_mean
        gsr_response_count = len(window['gsr_raw'][window['gsr_raw'].diff() > 0])

        # Combine features into a dictionary
        features = {
            'ppg_mean': ppg_mean,
            'ppg_std': ppg_std,
            'ppg_max': ppg_max,
            'ppg_min': ppg_min,
            'ppg_range': ppg_range,
            'ppg_rms': ppg_rms,
            'ppg_peaks': ppg_peaks,
            'gsr_mean': gsr_mean,
            'gsr_std': gsr_std,
            'gsr_max': gsr_max,
            'gsr_min': gsr_min,
            'gsr_range': gsr_range,
            'gsr_rms': gsr_rms,
            'gsr_peaks': gsr_peaks,
            'gsr_amplitude': gsr_amplitude,
            'gsr_response_count': gsr_response_count
        }

        features_list.append(features)

    return pd.DataFrame(features_list)

# Runs the model on the data written in a csv every 10 seconds
# Reads data, extracts features, and predicts stress level, and then waits 10 seconds until it reads again
def realtime_stress_detection(input_csv, interval=10):
    """
    Perform real-time stress detection every interval seconds. Default is 10 seconds for the interval.
    """
    print("Starting real-time stress detection...")
    last_processed_time = 0

    while True:
        try:
            # Load the latest data from the CSV file
            data = pd.read_csv(input_csv)
            
            # Filter data for the last 10 seconds
            current_time = data['timestep'].max()
            recent_data = data[data['timestep'] > (current_time - interval)]

            if not recent_data.empty:
                features = preprocess_and_extract_features(recent_data)
                predictions = model.predict(features)
                
                # Determine the most common prediction between choices of "stressed" and "not_stressed"
                # If there is a tie, we default to "not_stressed"
                counts = Counter(predictions)
                most_common = counts.most_common()
                most_common_prediction = "not_stressed" if len(most_common) > 1 and most_common[0][1] == most_common[1][1] else most_common[0][0]
                stress_result = "Stressed" if most_common_prediction == "stressed" else "Not Stressed"

                # Output the result
                print(f"Time: {current_time:.2f}s | Stress Status: {stress_result}")

                # Update the last processed time
                last_processed_time = current_time

            # Wait for the next interval
            time.sleep(interval)

        except KeyboardInterrupt:
            print("Real-time stress detection stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

# Main function
# Replace input_csv with the path to CSV file
# Might need to tweak this methodology if we are not reading from a CSV
if __name__ == "__main__":
    input_csv = "../data/live_data.csv"  
    realtime_stress_detection(input_csv)
