import cv2
import os


def display_images(original_dir, processed_dir):
    for filename in os.listdir(original_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            # Load the original and processed images
            original_path = os.path.join(original_dir, filename)
            processed_path = os.path.join(processed_dir, filename)

            original_image = cv2.imread(original_path)
            processed_image = cv2.imread(processed_path)

            if original_image is None or processed_image is None:
                continue

            # Resize for consistent display if necessary
            processed_image = cv2.resize(processed_image, (original_image.shape[1], original_image.shape[0]))

            # Concatenate images horizontally
            comparison_image = cv2.hconcat([original_image, processed_image])

            # Display the concatenated image
            cv2.imshow('Original vs. Processed', comparison_image)

            # Wait for a key press to move to the next image
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

