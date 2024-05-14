import cv2

def visualize_text_annotations(image_path, annotation_file, save_path):
  """
  Visualizes text annotations from a file and saves the image.

  Args:
    image_path: Path to the image file.
    annotation_file: Path to the text file containing annotations.
    save_path: Path to save the visualized image.
  """
  # Read image
  image = cv2.imread(image_path)

  # Read annotations
  annotations = []
  with open(annotation_file, 'r') as f:
    for line in f:
      # Parse annotations based on your format (example: class_name x_min y_min x_max y_max)
      class_name, x_min, y_min, x_max, y_max = line.strip().split()
      annotations.append((class_name, (int(x_min), int(y_min)), (int(x_max), int(y_max))))

  # Draw text on image for each annotation
  font = cv2.FONT_HERSHEY_SIMPLEX
  font_scale = 0.7
  font_thickness = 2
  for class_name, top_left, bottom_right in annotations:
    text_size, _ = cv2.getTextSize(class_name, font, font_scale, font_thickness)
    text_origin = (top_left[0], top_left[1] - text_size[1])  # Adjust based on text size
    cv2.putText(image, class_name, text_origin, font, font_scale, (0, 255, 0), font_thickness)

  # Save the visualized image  
  cv2.imwrite(save_path, image)

# Example usage (replace with your paths and annotation format)
image_path = "path/to/image.jpg"
annotation_file = "path/to/text_annotations.txt"
save_path = "path/to/save_annotated_image.jpg"

visualize_text_annotations(image_path, annotation_file, save_path)
