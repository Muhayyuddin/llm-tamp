import pybullet as p
import pybullet_data
from ultralytics import YOLO
import numpy as np
import cv2
import time
from envs.pb_env import PybulletEnv


class YOLOv8Detector(PybulletEnv):
    def __init__(self, model_path="./assets/best.pt"):
        super().__init__()

        # Load the YOLOv8 model
        self.model = YOLO(model_path)
        # Get the class names from the model
        self.class_names = self.model.names

    def detect(self, image):
        # Convert image to the required format (YOLOv8 works with PIL format, so we use cv2 to PIL conversion)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # YOLOv8 expects an RGB image
        results = self.model(image_rgb)  # Perform inference

        # Initialize lists to store final detection results
        final_boxes, final_labels, final_scores = [], [], []

        # Loop through results
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()  # Extract bounding box coordinates
            confidences = result.boxes.conf.cpu().numpy()  # Extract confidence scores
            class_ids = result.boxes.cls.cpu().numpy().astype(int)  # Extract class labels (as integers)

            # Filter by confidence threshold (similar to 0.5 confidence in the original function)
            for i, conf in enumerate(confidences):
                if conf > 0.1:
                    box = boxes[i]
                    class_id = class_ids[i]
                    label = self.class_names[class_id]  # Convert class ID to label text
                    final_boxes.append(box.astype(int).tolist())  # Convert to list of integers
                    final_labels.append(label)  # Append label as text
                    final_scores.append(conf)

        return {'boxes': final_boxes, 'labels': final_labels, 'scores': final_scores}

    def draw_detections(self, image, detection_results):
        """
        Draw bounding boxes and labels on the image.
        """
        # Loop through detected objects and draw the boxes and labels
        for label, box in zip(detection_results['labels'], detection_results['boxes']):
            # Get bounding box coordinates
            xmin, ymin, xmax, ymax = box

            # Draw the bounding box
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=(0, 255, 0), thickness=2)

            # Put the label text on the image
            label_text = f"{label}"
            cv2.putText(image, label_text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        return image

    def save_detections_to_file(self, image, detection_results, file_path):
        """
        Save the input image and detection results to a text file.
        """
        # Save the image to disk
        image_path = file_path.replace('.txt', '.jpg')
        cv2.imwrite(image_path, image)

        # Save the bounding boxes and labels to a text file
        with open(file_path, 'w') as f:
            for label, box in zip(detection_results['labels'], detection_results['boxes']):
                f.write(f"{label} {box[0]} {box[1]} {box[2]} {box[3]}\n")

        print(f"Detections saved to {file_path} and image saved to {image_path}")

    def read_detections_from_file(self, file_path):
        """
        Read the image and detection results from a text file and display them.
        """
        # Load the image
        image_path = file_path.replace('.txt', '.jpg')
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Load the bounding boxes and labels
        detections = []
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                label = parts[0]
                box = list(map(int, parts[1:]))
                detections.append((label, box))

        # Draw detections on the image
        for label, box in detections:
            xmin, ymin, xmax, ymax = box
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=(0, 255, 0), thickness=2)
            label_text = f"{label}"
            cv2.putText(image, label_text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Display the image
        cv2.imshow("Detections from File", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def setup_pybullet_camera(self):
        """
        Set up a PyBullet camera with ZED2i parameters.
        """
        width, height = 1280, 720
        fov = 90  # Field of view
        aspect = width / height
        near_plane, far_plane = 0.1, 100

        camera_position = [0.5, 0, 0.5]  # Adjust as needed
        target_position = [0.5, 0, 0]
        up_vector = [0, 1, 0]
        view_matrix = p.computeViewMatrix(camera_position, target_position, up_vector)

        projection_matrix = p.computeProjectionMatrixFOV(fov, aspect, near_plane, far_plane)
        return view_matrix, projection_matrix, width, height

    def get_camera_image(self, view_matrix, projection_matrix, width, height):
        """
        Capture an image from the PyBullet camera and ensure it's OpenCV compatible.
        """
        _, _, rgb_image, _, _ = p.getCameraImage(
            width=width,
            height=height,
            viewMatrix=view_matrix,
            projectionMatrix=projection_matrix,
            renderer=p.ER_BULLET_HARDWARE_OPENGL
        )
        # Convert the image to a numpy array (PyBullet returns a flat RGBA array)
        rgb_image = np.array(rgb_image, dtype=np.uint8).reshape((height, width, 4))[:, :, :3]
        # Convert RGB to BGR for OpenCV compatibility
        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        return bgr_image


# if __name__ == "__main__":
#     # Set up PyBullet
#     p.connect(p.GUI)
#     p.setAdditionalSearchPath(pybullet_data.getDataPath())
#     p.loadURDF("plane.urdf")

#     p.loadURDF("/home/muhayy/miniconda3/envs/llm_env/lib/python3.10/site-packages/pybullet_data/urdf/cup/cup.urdf", [0.4, 0.0, 0.05])
#     p.loadURDF("/home/muhayy/miniconda3/envs/llm_env/lib/python3.10/site-packages/pybullet_data/urdf/banana/banana.urdf", [0.0, 0.0, 0.05])

#     # Set up the camera
#     view_matrix, projection_matrix, width, height = setup_pybullet_camera()

#     # Initialize the YOLOv8 detector
#     detector = YOLOv8Detector()

#     try:
#         while True:
#             # Capture an image from the PyBullet camera
#             camera_image = get_camera_image(view_matrix, projection_matrix, width, height)

#             # Ensure the image is correctly formatted for OpenCV
#             camera_image = camera_image.astype(np.uint8)

#             # Detect objects in the image
#             results = detector.detect(camera_image)

#             # Draw detections on the image
#             image_with_detections = detector.draw_detections(camera_image, results)

#             # Display the image with detections
#             cv2.imshow("YOLOv8 Detections", image_with_detections)

#             # Break loop and close window when ESC is pressed
#             if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for the ESC key
#                 break

#             # Add a small delay for better visualization
#             time.sleep(0.1)

#     finally:
#         cv2.destroyAllWindows()
#         p.disconnect()
