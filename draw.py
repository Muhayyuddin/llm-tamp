import cv2
# detection
def draw_detections(image_path, labels_file, output_path):
    """
    Draw bounding boxes and labels on the image using OpenCV.

    :param image_path: Path to the input image (JPG format)
    :param labels_file: Path to the text file with label and bounding box data
    :param output_path: Path to save the output image
    """
    try:
        # Load the image
        image = cv2.imread(image_path)

        # Read the bounding boxes and labels from the file
        with open(labels_file, 'r') as file:
            for line in file:
                # Split the line into components
                parts = line.strip().split()
                if len(parts) >= 5:
                    label = parts[0]
                    xmin, ymin, xmax, ymax = map(int, parts[1:])

                    # Draw the bounding box
                    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=(0, 255, 0), thickness=2)

                    # Draw the label text above the bounding box
                    label_text = f"{label}"
                    cv2.putText(image, label_text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.9, color=(255, 255, 255), thickness=2)

        # Save the output image
        cv2.imwrite(output_path, image)
        print(f"Output image saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
image_path = "detections.jpg"  # Replace with your input image path
labels_file = "detections.txt"  # Replace with your labels text file path
output_path = "output_cv2.jpg"  # Path to save the output image

draw_detections(image_path, labels_file, output_path)

