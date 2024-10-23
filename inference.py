import os
import subprocess

def inference(yolvo7_path, images_dir, inference_dir, weights_path):
    os.chdir(yolvo7_path)
    for folder_name in os.listdir(images_dir):
        folder_path = os.path.join(images_dir, folder_name)
        
        if os.path.isdir(folder_path):

            output_folder = os.path.join(inference_dir, folder_name)           
            
            # Run YOLOv7 inference command
            command = [
                "python", "detect.py",
                "--save-txt",
                "--save-txt-coor",
                "--save-conf",
                "--weights", weights_path,
                "--source", folder_path,
                "--name", output_folder
            ]
            
            print(f"Running inference for {folder_name}...")
            subprocess.run(command)
            print(f"Inference for {folder_name} completed and saved to {output_folder}")
