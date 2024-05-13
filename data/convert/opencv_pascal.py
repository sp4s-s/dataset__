from xml.etree import ElementTree as ET

def convert_opencv_to_voc(txt_path, xml_path):
  """
  Converts annotations from OpenCV text format to Pascal VOC XML format.

  Args:
      txt_path (str): Path to the OpenCV text annotation file.
      xml_path (str): Path to save the converted Pascal VOC XML annotations.
  """

  # Open text file
  with open(txt_path) as f:
    lines = f.readlines()

  # Parse image dimensions (assuming the first line contains width and height)
  try:
    width, height = map(int, lines[0].strip().split())
  except (IndexError, ValueError):
    raise ValueError("Invalid OpenCV text format (missing or invalid dimensions)")

  # Create the XML root element
  annotation = ET.Element('annotation')

  # Add folder element (optional, modify if needed)
  folder = ET.SubElement(annotation, 'folder')
  folder.text = 'undefined'

  # Add filename element
  filename = ET.SubElement(annotation, 'filename')
  filename.text = os.path.basename(txt_path).split('.')[0]  # Extract filename (assuming format)

  # Add source element (optional)
  source = ET.SubElement(annotation, 'source')
  database = ET.SubElement(source, 'database')
  database.text = 'Unknown'

  # Add size element
  size = ET.SubElement(annotation, 'size')
  width_el = ET.SubElement(size, 'width')
  width_el.text = str(width)
  height_el = ET.SubElement(size, 'height')
  height_el.text = str(height)
  depth_el = ET.SubElement(size, 'depth')
  depth_el.text = '3'  # Assuming RGB image

  # Add segmented element (set to 0 for single objects)
  segmented = ET.SubElement(annotation, 'segmented')
  segmented.text = '0'

  # Loop through remaining lines (assuming each line represents a polygon)
  for line in lines[1:]:
    # Extract polygon points as comma-separated integers
    points_str = line.strip()
    points = list(map(int, points_str.split(',')))

    # Validate polygon format (should have 8 points for rectangle)
    if len(points) != 8:
      raise ValueError("Invalid OpenCV text format (polygon should have 8 points)")

    # Create object element
    obj = ET.SubElement(annotation, 'object')

    # Add name element (assuming class name is not provided, set to 'unknown')
    name = ET.SubElement(obj, 'name')
    name.text = 'unknown'

    # Add pose element (optional)
    pose = ET.SubElement(obj, 'pose')
    pose.text = 'Unspecified'

    # Add bndbox element
    bndbox = ET.SubElement(obj, 'bndbox')
    xmin_el = ET.SubElement(bndbox, 'xmin')
    xmin_el.text = str(points[0])
    ymin_el = ET.SubElement(bndbox, 'ymin')
    ymin_el.text = str(points[1])
    xmax_el = ET.SubElement(bndbox, 'xmax')
    xmax_el.text = str(points[2])
    ymax_el = ET.SubElement(bndbox, 'ymax')
    ymax_el.text = str(points[3])

  # Write the XML tree to file
  tree = ET.ElementTree(annotation)
  with open(xml_path, 'wb') as f:
    tree.write(f)

# Example usage
txt_path = "image.txt"
xml_path = "image.xml"

convert_opencv_to_voc(txt_path, xml_path)
