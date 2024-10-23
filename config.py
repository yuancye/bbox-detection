import os 

root = os.getcwd()
metafile = os.path.join(root, '240724-peptides-metadata.xlsx')
sheet_name='rec_metadata_240827'
interested_drugs = ['PYY(3-36)-15']


video_folder = os.path.join(root, 'videos')

des_video_folder = os.path.join(root, 'video-duplicates')
os.makedirs(des_video_folder, exist_ok=True)

image_folder = os.path.join(root, 'frames')
os.makedirs(image_folder, exist_ok=True)

image_cropped_folder = os.path.join(root, 'frames-cropped')
os.makedirs(image_folder, exist_ok=True)

inference_folder = os.path.join(root, 'inference')
weights_path = os.path.join(root, '\yolov7\runs\train\yolov7-mouse-9735-640\weights\best_mouse-12457-640.pt')
os.makedirs(inference_folder, exist_ok=True)

results_folder = os.path.join(root, 'results')

csv_path = os.path.join(root, 'distance.csv')