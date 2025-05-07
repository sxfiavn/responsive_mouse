# model/stress_model.py

import pandas as pd
import numpy as np
import joblib
from collections import Counter
from config import USE_MOCK_MODEL

# Description: Model is loaded here, used in monitor_stress.py


if not USE_MOCK_MODEL:
    import joblib
    model = joblib.load("model/stress_classifier.pkl")
else:
    # Mocked model
    class MockModel:
        def predict(self, X):
            return ["stressed" if np.random.rand() < 0.9 else "not_stressed" for _ in range(len(X))]
            # return ["stressed" if np.random.rand() < 0.5 else "not_stressed" for _ in range(len(X))]

    model = MockModel()


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


def run_model(raw_buffer):
    df = pd.DataFrame(raw_buffer, columns=["ppg_raw", "gsr_raw", "timestamp"])
    df = df[["ppg_raw", "gsr_raw"]]

    features = preprocess_and_extract_features(df)

    if features.empty:
        return "not_stressed"

    predictions = model.predict(features)
    if len(predictions) == 0:
        return "not_stressed"  

    counts = Counter(predictions)
    if not counts:
        return "not_stressed"

    return counts.most_common(1)[0][0]