import os
import time
from pathlib import Path
import torch
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
import cv2

from model.u2net import U2NET_full

# Setup CUDA device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"Using device: {device}")

# Load model using the U2NET_full function which handles the configuration
model = U2NET_full().to(device)
model.eval()  # Set the model to evaluation mode

input_dir = 'images/'
output_dir = 'output/'

# Ensure the output directory exists
Path(output_dir).mkdir(parents=True, exist_ok=True)

# Initialize lists to hold file sizes and processing times for each category
small_files_metadata_cuda = {'count': 0, 'total_size': 0, 'total_time': 0}
large_files_metadata_cuda = {'count': 0, 'total_size': 0, 'total_time': 0}


# Image transformation function
def transform_image(image):
    """Resize images while preserving aspect ratio and using high-quality downsampling."""
    max_size = 1024  # Max size to which an image is resized
    if max(image.width, image.height) > max_size:
        scaling_factor = max_size / max(image.width, image.height)
        new_size = (int(image.width * scaling_factor), int(image.height * scaling_factor))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    return transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])(image).unsqueeze(0)


def remove_background_cuda(image_path):
    input_path = os.path.join(input_dir, image_path)
    output_path = os.path.join(output_dir, image_path)

    # Load and preprocess image
    img = Image.open(input_path).convert('RGB')
    img_tensor = transform_image(img).to(device)

    # Process the image and track the time taken
    start_time = time.time()
    with torch.no_grad():
        output = model(img_tensor)[0]
    end_time = time.time()
    processing_time = end_time - start_time

    # Create mask and apply to image
    mask = (output > 0.7).float().squeeze(0)  # Squeeze to remove batch dimension
    mask_np = mask.cpu().numpy()[0]  # Convert to numpy array
    mask_np = cv2.GaussianBlur(mask_np, (21, 21), 11)  # Apply Gaussian blur to smooth the mask
    mask_np = (mask_np * 255).astype(np.uint8)  # Convert to uint8
    img_np = np.array(img)
    if img_np.shape[:2] != mask_np.shape:  # Check if the mask and image are the same size
        mask_np = cv2.resize(mask_np, (img_np.shape[1], img_np.shape[0]))  # Resize the mask to match the image
    foreground = cv2.bitwise_and(img_np, img_np, mask=mask_np)

    # Save the result
    Image.fromarray(foreground).save(output_path, quality=95)

    file_size = os.path.getsize(output_path)
    return file_size, processing_time
