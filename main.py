import os
import time
from tqdm import tqdm
from pathlib import Path
from rembg import remove
from display_images import display_images
from tabulate import create_table

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


# Process each image and categorize by size
for image_file in tqdm(os.listdir(input_dir)):
    if image_file.endswith(('.png', '.jpg', '.jpeg')):
        file_size, processing_time = remove_background(image_file)
        # Categorize by size and accumulate data
        if file_size <= 100 * 1024:  # 100KB and under
            small_files_metadata['count'] += 1
            small_files_metadata['total_size'] += file_size
            small_files_metadata['total_time'] += processing_time
        elif file_size <= 5 * 1024 * 1024:  # 1-5MB
            large_files_metadata['count'] += 1
            large_files_metadata['total_size'] += file_size
            large_files_metadata['total_time'] += processing_time

# Calculate averages for each category
if small_files_metadata['count'] > 0:
    small_files_avg_size = small_files_metadata['total_size'] / small_files_metadata['count']
    small_files_avg_time = small_files_metadata['total_time'] / small_files_metadata['count']
else:
    small_files_avg_size = small_files_avg_time = 0

if large_files_metadata['count'] > 0:
    large_files_avg_size = large_files_metadata['total_size'] / large_files_metadata['count']
    large_files_avg_time = large_files_metadata['total_time'] / large_files_metadata['count']
else:
    large_files_avg_size = large_files_avg_time = 0

# Pass the averages to create_table function from tabulate.py
# Assuming create_table is adjusted to take these averages and print a table accordingly
create_table(small_files_metadata['count'], small_files_avg_size, small_files_avg_time,
             small_files_metadata['total_time'], large_files_metadata['count'], large_files_avg_size,
             large_files_avg_time, large_files_metadata['total_time'])

# Display the images
display_images(input_dir, output_dir)
