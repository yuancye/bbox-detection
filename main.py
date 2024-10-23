from config import *
from extract_videos import extract_video_name, copy_videos
from extract_frames import extract_frames
from crop_images import crop_images
from inference import inference
from process_inference_results import process_inference_results


if __name__ == '__main__':
  
    required_videos = extract_video_name(metafile, sheet_name, interested_drugs)

    copy_videos(video_folder, required_videos, des_video_folder)

    extract_frames(des_video_folder, image_folder, frame_interval=15)
    
    crop_images(image_folder, image_cropped_folder, start_y=0, fixed_w=1350, fixed_h=1100)

    inference(image_folder, inference_folder, weights_path)

    total_distances_df = process_inference_results(inference_folder, results_folder, create_video=False, display_trajecotry=True)  # You can adjust the fps as needed
    total_distances_df.to_csv(csv_path, index=False)

  
    