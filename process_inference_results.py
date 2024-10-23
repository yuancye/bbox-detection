
from pathlib import Path
from typing import Dict, List
import cv2
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def process_inference_results(src_base_dir, des_base_dir, create_video = True, display_trajecotry=False):
    total_distances = []
    distance_means = []
    video_names = []
    for root, folders, files in os.walk(src_base_dir):
        
        for file in files:
            
            # process images
            if create_video and file.endswith(('.png', '.jpg', '.jpeg')):  
                video_name = os.path.basename(root)                                        
                output_video_path = os.path.join(des_base_dir, video_name + '.avi')
                create_video_from_images(root, output_video_path, fps=30)               
                break

            # process bbox
            if file.endswith('.txt'):                
                parent_folder_name = os.path.basename(os.path.dirname(root))
                video_names.append(parent_folder_name)
                output_csv_path = os.path.join(des_base_dir, parent_folder_name + '.csv')
                df, total_distance, distance_mean = create_df_from_txt(root, output_csv_path)
                total_distances.append(total_distance)
                distance_means.append(distance_mean)
                if display_trajecotry:
                    output_image_name = os.path.join(des_base_dir, parent_folder_name + '.png')
                    _draw_colored_trajectory(df, output_image_name)
                
                break
    df = pd.DataFrame({'video_name': video_names, 'distances_total': total_distances, 'distance_mean' : distance_means})
    return df

def create_video_from_images(image_folder, output_video_path, fps=30):
    images = []
    
    # Get all the image filenames from the folder
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(image_folder, filename)
            images.append(img_path)

    # Check if there are any images
    if not images:
        print("No images found in the folder!")
        return
    
    # Read the first image to get the dimensions (width, height)
    first_image = cv2.imread(images[0])
    height, width, layers = first_image.shape

    # Create the video writer object
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Define the codec
    video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Iterate through all images and write them to the video
    for image_path in images:
        img = cv2.imread(image_path)
        video.write(img)

    # Release the video writer
    video.release()
    print(f"Video saved to {output_video_path}")

def create_df_from_txt(folder_path, output_csv_path):
    # Initialize an empty list to collect data
    data = []

    # Loop through all .txt files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            # Extract frame_id from the filename
            frame_id = os.path.splitext(filename)[0].split('_')[1]  # Get the part before the first underscore

            # Construct the full path to the txt file
            file_path = os.path.join(folder_path, filename)

            # Read the content of the txt file
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split()  # Split the line into parts
                    if len(parts) >= 5:  # Check if we have at least 5 values
                        # Extract the class ID, coordinates, and confidence score
                        cls = parts[0]
                        x_min = int(parts[1])
                        y_min = int(parts[2])
                        x_max = int(parts[3])
                        y_max = int(parts[4])
                        confidence = float(parts[5])

                        # Append the data to the list
                        data.append([frame_id, x_min, y_min, x_max, y_max, confidence])

    # Create a DataFrame from the collected data
    columns = ["frame_id", "x_min", "y_min", "x_max", "y_max", "confidence"]
    
    df = pd.DataFrame(data, columns=columns)
    df['frame_id'] = df['frame_id'].astype(int)

    df = df.sort_values(by='frame_id')

    # calculate the distance between two adjacent frames
    df['center_x'] = (df['x_min'] + df['x_max']) / 2
    df['center_y'] = (df['y_min'] + df['y_max']) / 2

    # Calculate the distance moved from the previous frame
    df['distance'] = np.sqrt((df['center_x'] - df['center_x'].shift(1)).pow(2) + 
                              (df['center_y'] - df['center_y'].shift(1)).pow(2))
    total_distance = df['distance'].sum()
    distance_mean = df['distance'].mean()
    # # Drop the temporary center columns
    # df = df.drop(columns=['center_x', 'center_y'])
    df.to_csv(output_csv_path, index=False)
    
    return df,  total_distance, distance_mean

def _calculate_distances(df):
    # Calculate distances between consecutive center points
    distances = np.sqrt(np.diff(df['center_x'])**2 + np.diff(df['center_y'])**2)
    # Prepend a zero for the first frame since it has no previous frame
    distances = np.concatenate(([0], distances))
    return distances

def _draw_colored_trajectory(df, output_image_name, x_ticks = np.arange(0, 1400, 200), y_ticks = np.arange(0, 1200, 200)):
    # Calculate distances
    distances = _calculate_distances(df)
    
    # Normalize distances to range [0, 1] for color mapping
    norm_distances = (distances - np.min(distances)) / (np.max(distances) - np.min(distances))
    
    # Create a new figure
    plt.figure(figsize=(10, 6))

    # Draw trajectory lines with colors based on distances
    for i in range(1, len(df)):
        plt.plot(df['center_x'].iloc[i-1:i+1], df['center_y'].iloc[i-1:i+1], 
                 color=cm.viridis(norm_distances[i]), linewidth=2)

    # Scatter plot for start point
    plt.scatter(df['center_x'].iloc[0], df['center_y'].iloc[0], color='red', s=100, label='Start Point', edgecolor='black')

    # Scatter plot for end point
    plt.scatter(df['center_x'].iloc[-1], df['center_y'].iloc[-1], color='blue', s=100, label='End Point', edgecolor='black')

    # Create a color bar
    scatter = plt.scatter(df['center_x'], df['center_y'], c=norm_distances, cmap='viridis', s=10)
    plt.colorbar(scatter, label='Movement Distance')

    plt.title('Trajectory of the Mouse with Movement Distances')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    # Apply the ticks to the axes
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)
    plt.grid()
    plt.legend()
    plt.savefig(output_image_name)
    # plt.show()


    plt.close()




