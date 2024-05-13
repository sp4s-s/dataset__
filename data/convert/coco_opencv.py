import json

def convert_coco_to_opencv(json_path, txt_path):
  """
  Converts annotations from COCO JSON format to OpenCV text format.

  Args:
      json_path (str): Path to the COCO JSON annotation file.
      txt_path (str): Path to save the converted OpenCV text annotations.
  """

  # Load COCO annotations
  with open(json_path) as f:
    coco_annotations = json.load(f)

  # Open text file for writing
  with open(txt_path, 'w') as f:
    # Loop through COCO images
    for img in coco_annotations["images"]:
      # Get image dimensions
      width = img["width"]
      height = img["height"]

      # Write image dimensions to the first line (optional)
      f.write(f"{width} {height}\n")

      # Loop through COCO annotations for this image
      for ann in coco_annotations["annotations"]:
        if ann["image_id"] != img["id"]:
          continue  # Skip annotations for other images

        # Get bounding box coordinates
        bbox = ann["bbox"]
        xmin = bbox[0]
        ymin = bbox[1]
        xmax = xmin + bbox[2]  # Convert to OpenCV format (xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax)
        ymax = ymin + bbox[3]

        # Write polygon points in OpenCV format
        f.write(f"{xmin} {ymin} {xmax} {ymin} {xmax} {ymax} {xmin} {ymax}\n")

# Example usage
json_path = "image.json"
txt_path = "image.txt"

convert_coco_to_opencv(json_path, txt_path)
