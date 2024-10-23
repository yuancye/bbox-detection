import os, cv2

def extract_frames(video_folder, ouotput_base, frame_interval=30):
    for file in os.listdir(video_folder):
        if file.endswith(('.avi', '.mp4')):
            video_path = os.path.join(video_folder, file)
            print(f'processing: {file}')
            filename_prefix = os.path.splitext(file)[0]
            
            output_folder = os.path.join(ouotput_base, filename_prefix)
            os.makedirs(output_folder, exist_ok=True)
            
            video_capture = cv2.VideoCapture(video_path)
            frame_count = 0
            while video_capture.isOpened():
                ret, frame = video_capture.read()
                if not ret:
                    break 

                if frame_count % frame_interval == 0:

                    frame_filename = os.path.join(output_folder, f'{filename_prefix}_{frame_count}.jpg')
                    #{frame_count:05d}
                    cv2.imwrite(frame_filename, frame)

                frame_count += 1
            video_capture.release()
            # os.remove(video_path)

    cv2.destroyAllWindows()

