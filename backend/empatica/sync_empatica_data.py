import pandas as pd
import os

def sync_empatica_data(subject_dir):

    data = pd.read_csv(os.path.join(subject_dir, 'data.csv'), sep=';', encoding='latin1')
    bvp = pd.read_csv(os.path.join(subject_dir, 'bvp.csv'), sep=',')
    peaks = pd.read_csv(os.path.join(subject_dir, 'systolic_peaks.csv'), sep=',')
    eda = pd.read_csv(os.path.join(subject_dir, 'eda.csv'), sep=',')
    
    video_start_ts = data['Session Start Timestamp'].iloc[0]
    video_end_ts = data['Session End Timestamp'].iloc[0]
    
    bvp = bvp[(bvp.unix_timestamp >= video_start_ts * 10**6) & (bvp.unix_timestamp <= video_end_ts * 10**6)]
    peaks = peaks[(peaks.systolic_peak_timestamp >= video_start_ts * 10**9) & (peaks.systolic_peak_timestamp <= video_end_ts * 10**9)]
    eda = eda[(eda.unix_timestamp >= video_start_ts * 10**6) & (eda.unix_timestamp <= video_end_ts * 10**6)]

    if bvp.empty or peaks.empty or eda.empty:
        raise ValueError("Nessun dato Empatica rimasto durante la sincronizzazione dei dati RAW con il video, sono stati scaricati i dati sbagliati?")
    
    bvp.to_csv(os.path.join(subject_dir, 'bvp.csv'), index=False)
    peaks.to_csv(os.path.join(subject_dir, 'systolic_peaks.csv'), index=False)
    eda.to_csv(os.path.join(subject_dir, 'eda.csv'), index=False)