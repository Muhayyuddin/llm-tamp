from ultralytics import YOLO
import numpy as np
import cv2
# Perception class
class YOLOv8Detector:
    def __init__(self, model_path='best.pt'):
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
        print(results)
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


    def preprocess_env_state_description(self, detection_results):
        """
        This function processes the detection output and returns the object list,
        bounding boxes, and estimated lengths in the format specified.
        """
        objects = []
        bounding_boxes = []
        lengths = []

        # Loop through detected objects
        for label, box in zip(detection_results['labels'], detection_results['boxes']):
            # Directly append the object name (which is already a label)
            objects.append(label)

            # Extract bounding box coordinates and add to the list
            xmin, ymin, xmax, ymax = box
            width = xmax - xmin
            height = ymax - ymin

            # Append bounding box (in [xmin, ymin, xmax, ymax] format)
            bounding_boxes.append([xmin, ymin, xmax, ymax])

            # Estimate lengths along x and y axes (simply using width and height of the bounding box)
            lengths.append([width, height])

        return objects, bounding_boxes, lengths

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


# if __name__ == "__main__":
#     # Load the image and run YOLOv8 for detection
#     detector = YOLOv8Detector()
#     image = cv2.imread('/home/mbzirc/llm-tamp/LLM-TAMP/perception/input_image.jpg')

#     # Detect objects in the image
#     results = detector.detect(image)

#     # Process the detection results into the desired format
#     objects, bounding_boxes, lengths = detector.preprocess_env_state_description(results)

#     # Output the results
#     print("Objects:", objects)
#     print("Bounding Boxes:", bounding_boxes)
#     print("Lengths:", lengths)

#     # Draw bounding boxes and labels on the image
#     image_with_detections = detector.draw_detections(image, results)

#     # Display the image with detections
#     while True:
#         cv2.imshow("Detections", image_with_detections)
#         # Break loop and close window when ESC is pressed
#         if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for the ESC key
#             break

#     cv2.destroyAllWindows()

