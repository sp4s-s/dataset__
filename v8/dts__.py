import json
import cv2
from pycocotools.coco import COCO
import numpy as np

def draw_annotations(image, annotations):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Example colors for different shapes
    for annotation in annotations:
        shape = annotation['shape']
        color = colors[shape]
        points = np.array(annotation['points'], np.int32)
        cv2.fillPoly(image, [points], color)

# Load COCO JSON annotations file
coco = COCO('annotations.json')  # Replace 'annotations.json' with your file path

# Load and draw annotations for each image
for img_id in coco.imgs:
    img_info = coco.loadImgs(img_id)[0]
    image = cv2.imread(img_info['file_name'])
    ann_ids = coco.getAnnIds(imgIds=img_id)
    annotations = coco.loadAnns(ann_ids)
    draw_annotations(image, annotations)
    
    # Save annotated image
    cv2.imwrite(f'annotated_{img_info["file_name"]}', image)

# Optional: Save annotations in a new JSON file
annotated_coco_data = coco.dataset
with open('annotated_annotations.json', 'w') as f:
    json.dump(annotated_coco_data, f)
