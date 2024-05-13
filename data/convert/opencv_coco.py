import json

def convert_opencv_to_coco(txt_path, image_id, image_file, coco_annotations):
  """
  Converts annotations from OpenCV text format to COCO JSON format structure.

  Args:
      txt_path (str): Path to the OpenCV text annotation file.
      image_id (int): Unique ID for the image (used in COCO annotations).
      image_file (str): Filename of the corresponding image.
      coco_annotations (dict): COCO annotations dictionary to populate (modified by reference).
  """

  # Open text file
  with open(txt_path) as f:
    lines = f.readlines()

  # Parse image dimensions (assuming the first line contains width and height)
  try:
    width, height = map(int, lines[0].strip().split())
  except (IndexError, ValueError):
    raise ValueError("Invalid OpenCV text format (missing or invalid dimensions)")

  # Loop through remaining lines (assuming each line represents a polygon)
  for idx, line in enumerate(lines[1:]):
    # Extract polygon points as comma-separated integers
    points_str = line.strip()
    points = list(map(int, points_str.split(',')))

    # Validate polygon format (should have 8 points for rectangle)
    if len(points) != 8:
      raise ValueError("Invalid OpenCV text format (polygon should have 8 points)")

    # Create COCO annotation dictionary
    annotation = {
        "id": len(coco_annotations["annotations"]) + 1,  # Unique annotation ID
        "image_id": image_id,
        "category_id": 1,  # Set category ID to 1 (modify if needed)
        "segmentation": [],  # Not used for bounding boxes (set to empty list)
        "area": 0,  # Area will be calculated
        "bbox": [],
        "iscrowd": 0  # Set to 0 for single objects
    }

    # Calculate area of the bounding box
    xmin = min(points[0::2])
    ymin = min(points[1::2])
    xmax = max(points[0::2])
    ymax = max(points[1::2])
    width = xmax - xmin
    height = ymax - ymin
    annotation["area"] = width * height

    # Set bounding box coordinates
    annotation["bbox"] = [xmin, ymin, width, height]

    # Add annotation to COCO annotations
    coco_annotations["annotations"].append(annotation)

  # Add image information to COCO annotations (if not already present)
  if image_file not in [img["file_name"] for img in coco_annotations["images"]]:
    coco_annotations["images"].append({
        "id": image_id,
        "width": width,
        "height": height,
        "file_name": image_file
    })

# Example usage (assuming you have a function to generate unique image IDs)
image_id = generate_unique_image_id()
image_file = "image.jpg"
coco_annotations = {"images": [], "annotations": []}

convert_opencv_to_coco("image.txt", image_id, image_file, coco_annotations)

# After processing all images, save COCO annotations to JSON file
with open("annotations.json", 'w') as f:
  json.dump(coco_annotations, f, indent=4)
