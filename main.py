import os
from tqdm import tqdm
from scripts.display_images import display_images
from scripts.tabulate import create_table
from scripts.remove_bg import remove_background, small_files_metadata, large_files_metadata
from scripts.remove_bg_cuda import remove_background_cuda, small_files_metadata_cuda, large_files_metadata_cuda

# Directory containing images
input_dir = 'images/'
output_dir = 'output/'


def process_images(remove_background_func, metadata):
    # Process each image and categorize by size
    for image_file in tqdm(os.listdir(input_dir)):
        if image_file.endswith(('.png', '.jpg', '.jpeg')):
            file_size, processing_time = remove_background_func(image_file)
            # Categorize by size and accumulate data
            if file_size < 1024 * 1024:  # Under 1MB
                metadata['count'] += 1
                metadata['total_size'] += file_size
                metadata['total_time'] += processing_time
            elif file_size <= 10 * 1024 * 1024:  # 1-10MB
                metadata['count'] += 1
                metadata['total_size'] += file_size
                metadata['total_time'] += processing_time


def calculate_averages(metadata):
    # Calculate averages for each category
    if metadata['count'] > 0:
        avg_size = metadata['total_size'] / metadata['count']
        avg_time = metadata['total_time'] / metadata['count']
    else:
        avg_size = avg_time = 0
    return avg_size, avg_time


# Process images without CUDA
print("Processing images without CUDA...")
process_images(remove_background, small_files_metadata)
small_files_avg_size, small_files_avg_time = calculate_averages(small_files_metadata)
large_files_avg_size, large_files_avg_time = calculate_averages(large_files_metadata)

# Display the table and images
create_table(small_files_metadata['count'], small_files_avg_size, small_files_avg_time,
             small_files_metadata['total_time'], large_files_metadata['count'], large_files_avg_size,
             large_files_avg_time, large_files_metadata['total_time'])
display_images(input_dir, output_dir)

# Process images with CUDA
print("\nProcessing images with CUDA...")
process_images(remove_background_cuda, small_files_metadata_cuda)
small_files_avg_size_cuda, small_files_avg_time_cuda = calculate_averages(small_files_metadata_cuda)
large_files_avg_size_cuda, large_files_avg_time_cuda = calculate_averages(large_files_metadata_cuda)

# Display the table and images
create_table(
    small_files_metadata_cuda['count'],
    small_files_avg_size_cuda,
    small_files_avg_time_cuda,
    small_files_metadata_cuda['total_time'],
    large_files_metadata_cuda['count'],
    large_files_avg_size_cuda,
    large_files_avg_time_cuda,
    large_files_metadata_cuda['total_time']
)
display_images(input_dir, output_dir)
