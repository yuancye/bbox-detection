import cv2
import os


def crop_images(image_base, output_folder, start_y=None, fixed_w=None, fixed_h=None):
    
    for root, folders, files in os.walk(image_base):
        for file in files: 
            if file.lower().endswith('.jpg'):
                first_image = cv2.imread(os.path.join(root, file))
                # Allow user to select ROI
                roi = cv2.selectROI("Select ROI", first_image, fromCenter=False, showCrosshair=True)
                cv2.destroyAllWindows()  # Close the ROI window

                x, _, _, _ = map(int, roi)
                des_folder = os.path.join(output_folder, os.path.basename(root))
                os.makedirs(des_folder, exist_ok=True)
                _crop_images(root, files, des_folder, x, start_y, fixed_w, fixed_h)
                break

def _crop_images(root, files, output_folder, x, y, w, h):
    
    for image_file in files:
        image_path = os.path.join(root, image_file)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Error: Could not load image {image_file}. Skipping.")
            continue

        cropped_image = image[y:y+h, x:x+w]

        output_path = os.path.join(output_folder, image_file)
        cv2.imwrite(output_path, cropped_image)

        print(f"Saved cropped image to {output_path}")

    print("Finished processing all images.")




