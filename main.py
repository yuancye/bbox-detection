import os 
from extract_videos import extract_video_name, copy_videos
from extract_frames import extract_frames
from crop_images import crop_images
from inference import inference
from process_inference_results import process_inference_results


if __name__ == '__main__':
    root = os.getcwd()
    metafile = os.path.join(root, '240724-peptides-metadata.xlsx')
    sheet_name='rec_metadata_240827'
    interested_drugs = ['CCK-8-sulfate-2']

    video_folder = os.path.join(root, 'videos')
   

    des_video_folder = os.path.join(root, 'video-duplicates')
    image_folder = os.path.join(root, 'frames')
    image_cropped_folder = os.path.join(root, 'frames-cropped')
    inference_folder = os.path.join(root, 'inference')
    results_folder = os.path.join(root, 'results')

    csv_path = os.path.join(root, 'cck-2.csv')
   
    weights_path = os.path.join(root, r'yolov7\runs\train\yolov7-mouse-9735-640\weights\best_mouse-12457-640.pt')
    yolvo7_path = os.path.join(root, 'yolov7')
    os.makedirs(des_video_folder, exist_ok=True)  
    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(inference_folder, exist_ok=True)
    os.makedirs(results_folder, exist_ok=True)
 
    required_videos = extract_video_name(metafile, sheet_name, interested_drugs)

    copy_videos(video_folder, required_videos, des_video_folder)

    extract_frames(des_video_folder, image_folder, frame_interval=15)
    
    crop_images(image_folder, image_cropped_folder, start_y=0, fixed_w=1350, fixed_h=1100)

    inference(yolvo7_path, image_cropped_folder, inference_folder, weights_path)

    total_distances_df = process_inference_results(inference_folder, results_folder, create_video=False, display_trajecotry=True)  # You can adjust the fps as needed
    total_distances_df.to_csv(csv_path, index=False)

  
    
