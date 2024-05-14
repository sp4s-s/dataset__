import xml.etree.ElementTree as ET
import cv2

def visualize_pascal(annotation_path, image_path, save_path):
  """
  Visualizes a Pascal VOC annotation and saves the image.

  Args:
    annotation_path: Path to the Pascal VOC annotation XML file.
    image_path: Path to the image file.
    save_path: Path to save the visualized image.
  """
  # Parse Pascal VOC annotations
  tree = ET.parse(annotation_path)
  root = tree.getroot()

  # Read image
  image = cv2.imread(image_path)

  # Loop through object annotations and draw bounding boxes
  for obj in root.findall('object'):
    name = obj.find('name').text
    bndbox = obj.find('bndbox')
    x_min = int(bndbox.find('xmin').text)
    y_min = int(bndbox.find('ymin').text)
    x_max = int(bndbox.find('xmax').text)
    y_max = int(bndbox.find('ymax').text)
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

  # Save the visualized image  
  cv2.imwrite(save_path, image)

# Example usage (replace with your paths)
annotation_path = "path/to/annotation.xml"
image_path = "path/to/image.jpg"
save_path = "path/to/save_annotated_image.jpg"

visualize_pascal(annotation_path, image_path, save_path)
