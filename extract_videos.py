import os, shutil
import pandas as pd

# read the metadate, find all the videos.

def extract_video_name(metafile, sheetname, interested_drugs) -> pd.DataFrame:
    metadata = pd.read_excel(metafile, sheet_name=sheetname, dtype={'recording_time': str})
    metadata['drug_high'] = metadata['drug'] + '-' + metadata['drug_dose_ug/kg'].astype(int).astype(str)
    filtered_metadata = metadata[metadata['drug_high'].isin(interested_drugs)]
    results = filtered_metadata[['drug_high', 'recording_time']]
    return results

def copy_videos(video_path, required_videos, des_folder):
    for root, folder, files in os.walk(video_path):
        for file in files:
            if '.avi' in file:
                video_name = file.split('-')[1]
                
                if video_name in required_videos['recording_time'].tolist():
                    print(video_name)
                    src_path = os.path.join(root, file)
                    drug_high = required_videos.loc[required_videos['recording_time'] == video_name, 'drug_high'].values[0]
                    output_video_name = f"{drug_high}-{video_name}.avi"
                    des_path = os.path.join(des_folder, output_video_name)
                    shutil.copy(src_path, des_path)

