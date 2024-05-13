from PIL import Image  # For image size
import json

def convert_coco_to_voc(json_path, image_path, xml_path):
  """
  Converts annotations from COCO JSON format to Pascal VOC XML format.

  Args:
      json_path (str): Path to the COCO JSON annotation file.
      image_path (str): Path to the corresponding image file.
      xml_path (str): Path to save the converted Pascal VOC XML annotations.
  """

  # Read image dimensions
  img = Image.open(image_path)
  width, height = img.size

  # Load COCO annotations
  with open(json_path) as f:
    coco_annotations = json.load(f)

  # Get image information from COCO annotations
  image_id = None
  for img in coco_annotations["images"]:
    if img["file_name"] == os.path.basename(image_path):  # Match by filename
      image_id = img["id"]
      break

  if image_id is None:
    raise ValueError("Image not found in COCO annotations")

  # Open XML file for writing
  with open(xml_path, 'w') as f:
    # Write XML header
    f.write('<annotation>\n')
    f.write(f'\t<folder>undefined</folder>\n')  # Modify if needed
    f.write(f'\t<filename>{os.path.basename(image_path)}</filename>\n')
    f.write(f'\t<source>\n')
    f.write('\t\t<database>Unknown</database>\n')
    f.write('\t</source>\n')
    f.write(f'\t<size>\n')
    f.write(f'\t\t<width>{width}</width>\n')
    f.write(f'\t\t<height>{height}</height>\n')
    f.write('\t\t<depth>3</depth>\n')  # Assuming RGB images
    f.write('\t</size>\n')
    f.write('\t<segmented>0</segmented>\n')  # Set to 0 for single objects

    # Loop through COCO annotations for this image
    for ann in coco_annotations["annotations"]:
      if ann["image_id"] != image_id:
        continue  # Skip annotations for other images

      category_id = ann["category_id"] - 1  # Match category ID starting from 0
      category_name = coco_annotations["categories"][category_id]["name"]

      # Get bounding box coordinates
      bbox = ann["bbox"]
      xmin = bbox[0]
      ymin = bbox[1]
      xmax = xmin + bbox[2]  # Convert to VOC format (xmin, ymin, xmax, ymax)
      ymax = ymin + bbox[3]

      # Write object annotation to XML
      f.write('\t<object>\n')
      f.write(f'\t\t<name>{category_name}</name>\n')
      f.write(f'\t\t<pose>Unspecified</pose>\n')
      f.write(f'\t\t<bndbox>\n')
      f.write(f'\t\t\t<xmin>{xmin}</xmin>\n')
      f.write(f'\t\t\t<ymin>{ymin}</ymin>\n')
      f.write(f'\t\t\t<xmax>{xmax}</xmax>\n')
      f.write(f'\t\t\t<ymax>{ymax}</ymax>\n')
      f.write('\t\t</bndbox>\n')
      f.write('\t</object>\n')

    # Close XML annotation
    f.write('</annotation>\n')

# Example usage
json_path = "image.json"
image_path = "image.jpg"
xml_path = "image.xml"

convert_coco_to_voc(json_path, image_path, xml_path)
