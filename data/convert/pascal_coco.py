from PIL import Image  # For image size
from collections import defaultdict
import json

def convert_voc_to_coco(xml_path, image_path, json_path):
  """
  Converts annotations from a Pascal VOC XML file to COCO JSON format.

  Args:
      xml_path (str): Path to the Pascal VOC XML annotation file.
      image_path (str): Path to the corresponding image file.
      json_path (str): Path to save the converted COCO JSON annotations.
  """

  # Read image dimensions
  img = Image.open(image_path)
  width, height = img.size

  # Initialize COCO annotations dictionary
  coco_annotations = {
      "images": [],
      "categories": [],
      "annotations": []
  }

  # Category id counter
  category_id = 1

  # Parse XML annotations
  with open(xml_path) as f:
    # Use ElementTree for XML parsing (assuming standard VOC format)
    from xml.etree import ElementTree as ET
    tree = ET.parse(f)
    root = tree.getroot()

    # Get image information
    filename = root.find('filename').text
    image_id = int(root.find('filename').text.split('.')[0])  # Extract image ID from filename (assuming format)

    # Add image information to COCO annotations
    coco_annotations["images"].append({
        "id": image_id,
        "width": width,
        "height": height,
        "file_name": filename
    })

    # Loop through objects in annotations
    for obj in root.findall('object'):
      name = obj.find('name').text

      # Add category if not already present
      if name not in coco_annotations["categories"]:
        coco_annotations["categories"].append({
            "id": category_id,
            "name": name,
            "supercategory": "none"  # Modify if needed
        })
        category_id += 1

      # Get bounding box coordinates
      bndbox = obj.find('bndbox')
      xmin = int(bndbox.find('xmin').text)
      ymin = int(bndbox.find('ymin').text)
      xmax = int(bndbox.find('xmax').text)
      ymax = int(bndbox.find('ymax').text)

      # Convert to COCO format (x, y, width, height)
      bbox = [xmin, ymin, xmax - xmin, ymax - ymin]

      # Add annotation to COCO annotations
      coco_annotations["annotations"].append({
          "id": len(coco_annotations["annotations"]) + 1,  # Unique annotation ID
          "image_id": image_id,
          "category_id": coco_annotations["categories"].index(name) + 1,  # Match category by name
          "segmentation": [],  # Not used for bounding boxes (set to empty list)
          "area": bbox[2] * bbox[3],  # Area of bounding box
          "bbox": bbox,
          "iscrowd": 0  # Set to 0 for single objects
      })

  # Save COCO annotations to JSON file
  with open(json_path, 'w') as outfile:
    json.dump(coco_annotations, outfile, indent=4)

# Example usage
xml_path = "image.xml"
image_path = "image.jpg"
json_path = "image.json"

convert_voc_to_coco(xml_path, image_path, json_path)
