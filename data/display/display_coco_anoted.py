import json
import cv2
from PIL import Image

def visualize_coco(coco_file, image_path, save_path):
  """
  Visualizes a COCO JSON annotated image and saves it.

  Args:
    coco_file: Path to the COCO JSON annotation file.
    image_path: Path to the image file.
    save_path: Path to save the visualized image.
  """
  # Read COCO annotations
  with open(coco_file) as f:
    annotations = json.load(f)

  # Read image
  image = cv2.imread(image_path)

  # Loop through annotations and draw bounding boxes
  for annotation in annotations["annotations"]:
    bbox = annotation["bbox"]
    x_min, y_min, width, height = bbox
    cv2.rectangle(image, (x_min, y_min), (x_min + width, y_min + height), (0, 255, 0), 2)

  # Convert OpenCV image to PIL format for saving
  pil_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  pil_image = Image.fromarray(pil_image)

  # Save the visualized image
  pil_image.save(save_path)

# Example usage (replace with your paths)
coco_file = "path/to/coco.json"
image_path = "path/to/image.jpg"
save_path = "path/to/save_annotated_image.jpg"

visualize_coco(coco_file, image_path, save_path)
