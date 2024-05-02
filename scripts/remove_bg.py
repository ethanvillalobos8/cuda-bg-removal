import os
import time
from pathlib import Path
from rembg import remove

# Directory containing images
input_dir = 'images/'
output_dir = 'output/'

# Ensure the output directory exists
Path(output_dir).mkdir(parents=True, exist_ok=True)

# Initialize lists to hold file sizes and processing times for each category
small_files_metadata = {'count': 0, 'total_size': 0, 'total_time': 0}
large_files_metadata = {'count': 0, 'total_size': 0, 'total_time': 0}


def remove_background(image_path):
    input_path = os.path.join(input_dir, image_path)
    output_path = os.path.join(output_dir, image_path)

    # Read the image and get its size
    with open(input_path, 'rb') as file:
        input_data = file.read()
        file_size = len(input_data)

    # Process the image and track the time taken
    start_time = time.time()
    output_data = remove(input_data)
    end_time = time.time()
    processing_time = end_time - start_time

    # Save the image
    with open(output_path, 'wb') as file:
        file.write(output_data)

    # print(f"Processed {image_path}")

    return file_size, processing_time

