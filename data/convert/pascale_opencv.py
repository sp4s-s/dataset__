from xml.etree import ElementTree as ET

def convert_voc_to_opencv(xml_path, txt_path):
  """
  Converts annotations from Pascal VOC XML format to OpenCV text format.

  Args:
      xml_path (str): Path to the Pascal VOC XML annotation file.
      txt_path (str): Path to save the converted OpenCV text annotations.
  """

  # Parse XML annotations
  with open(xml_path) as f:
    tree = ET.parse(f)
    root = tree.getroot()

  # Get image size (assuming size information is present)
  width = None
  height = None
  size = root.find('size')
  if size is not None:
    width = int(size.find('width').text)
    height = int(size.find('height').text)

  # Open text file for writing
  with open(txt_path, 'w') as f:
    # Write image dimensions to the first line (optional)
    if width and height:
      f.write(f"{width} {height}\n")

    # Loop through objects in annotations
    for obj in root.findall('object'):
      # Get bounding box coordinates
      bndbox = obj.find('bndbox')
      xmin = int(bndbox.find('xmin').text)
      ymin = int(bndbox.find('ymin').text)
      xmax = int(bndbox.find('xmax').text)
      ymax = int(bndbox.find('ymax').text)

      # Write polygon points in OpenCV format (xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax)
      f.write(f"{xmin} {ymin} {xmax} {ymin} {xmax} {ymax} {xmin} {ymax}\n")

# Example usage
xml_path = "image.xml"
txt_path = "image.txt"

convert_voc_to_opencv(xml_path, txt_path)
