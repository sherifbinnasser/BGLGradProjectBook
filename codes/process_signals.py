import cv2
import numpy as np
import pandas as pd
import os
from scipy.signal import resample, butter, filtfilt, detrend

# Configuration Paths
video_folder = r"G:\cleaned data"
output_folder = r"C:\Users\Mostafa Magdy\Desktop\processed_dataset"
data_csv_path = r"G:\cleaned data\data.csv"

os.makedirs(output_folder, exist_ok=True)
df = pd.read_csv(data_csv_path)

# Filter Parameters
fs = 20
lowcut = 0.5
highcut = 8.0

def extract_raw_rgb(video_path):
    cap = cv2.VideoCapture(video_path)
    R, G, B = [], [], []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Mean of full frame matrix (ROI = Full Frame)
        R.append(np.mean(frame[:, :, 2]))
        G.append(np.mean(frame[:, :, 1]))
        B.append(np.mean(frame[:, :, 0]))
    cap.release()
    return np.array(R), np.array(G), np.array(B)

def downsample_30_to_20(signal):
    target_length = int(len(signal) * 20 / 30)
    return resample(signal, target_length)

def signal_conditioning(signal, fs, low, high, order=4):
    # Detrend & Z-score Normalization
    detrended = detrend(signal)
    std = np.std(detrended)
    normalized = detrended if std == 0 else (detrended - np.mean(detrended)) / std
    
    # Butterworth Bandpass Filter
    nyq = 0.5 * fs
    b, a = butter(order, [low/nyq, high/nyq], btype='band')
    return filtfilt(b, a, normalized)

# Execution Loop over the verified dataset
for i in range(1, 249):
    video_name = f"patient{i}.mp4"
    video_path = os.path.join(video_folder, video_name)
    if not os.path.exists(video_path):
        continue

    # Extract & Standardize Frame Rate
    R, G, B = extract_raw_rgb(video_path)
    if i <= 93:  # Native 30fps hardware downsampled to 20fps
        R, G, B = downsample_30_to_20(R), downsample_30_to_20(G), downsample_30_to_20(B)

    # Force strict array synchronization (Length = 400)
    target_len = 400
    if len(R) != target_len:
        R, G, B = resample(R, target_len), resample(G, target_len), resample(B, target_len)

    # Apply Signal Detrending, Scaling, and Butterworth Bandpass Filter
    R_processed = signal_conditioning(R, fs, lowcut, highcut)
    G_processed = signal_conditioning(G, fs, lowcut, highcut)
    B_processed = signal_conditioning(B, fs, lowcut, highcut)

    # Export Stratified Tracking Sheets
    patient_row = df[df["id"] == i].iloc[0]
    output_df = pd.DataFrame({
        "id": [patient_row["id"]] * target_len,
        "name": [patient_row["name"]] * target_len,
        "age": [patient_row["age"]] * target_len,
        "gender": [patient_row["gender"]] * target_len,
        "R_value": R_processed,
        "G_value": G_processed,
        "B_value": B_processed,
        "glucose_level": [patient_row["glucose_level"]] * target_len
    })
    output_df.to_csv(os.path.join(output_folder, f"patient{i}.csv"), index=False)

print("Phase 3 Signal Extraction completed successfully!")