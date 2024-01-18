import glob
import json
import os
import cv2
import shutil

MASK_EXT = 'tif'
ORIGINAL_EXT = 'tif'
MASK_PATH = 'labels'
IMG_PATH = 'images'

def create_annotation_for_contour(contour, annotation_id: int, image_id):
    bbox = cv2.boundingRect(contour)
    area = cv2.contourArea(contour)
    segmentation = contour.flatten().tolist()

    annotation = {
        "iscrowd": 0,
        "id": annotation_id,
        "image_id": image_id,
        "category_id": 1,
        "bbox": bbox,
        "area": area,
        "segmentation": [segmentation],
    }

    return annotation


def contours_from_mask_image(mask_image_open):
    # Find contours in the mask image
    gray = cv2.cvtColor(mask_image_open, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    return contours


def images_annotations_info(path):
    """
    Process the binary masks and generate images and annotations information.

    :param path: Path to the directory containing images and binary masks
    :return: Tuple containing images info, annotations info, and annotation count
    """
    image_id = 0
    annotation_id = 0
    annotations = []
    images = []


    for mask_image in glob.glob(os.path.join(path, MASK_PATH, f'*.{MASK_EXT}')):
        original_file_name = f'{os.path.basename(mask_image).split(".")[0]}.{ORIGINAL_EXT}'
        mask_image_open = cv2.imread(mask_image)

        # Get image dimensions
        height, width, _ = mask_image_open.shape

        # Create or find existing image annotation
        if original_file_name not in map(lambda img: img['file_name'], images):
            image = {
                "id": image_id + 1,
                "width": width,
                "height": height,
                "file_name": original_file_name,
            }
            images.append(image)
            image_id += 1
        else:
            image = [element for element in images if element['file_name'] == original_file_name][0]

        contours = contours_from_mask_image(mask_image_open)

        # Create annotation for each contour
        for contour in contours:
            annotation = create_annotation_for_contour(contour, annotation_id, image['id'])

            # Add annotation if area is greater than zero
            if annotation["area"] > 0:
                annotations.append(annotation)
                annotation_id += 1

    return images, annotations, annotation_id


def process_masks(mask_path, dest_json):
    # Initialize the COCO JSON format with categories
    coco_format = {
        "info": {},
        "licenses": [],
        "images": [],
        "categories": [{"id": 1, "name": 'Vessel', "supercategory": 'Vessel'}],
        "annotations": [],
    }

    # Create images and annotations sections
    coco_format["images"], coco_format["annotations"], annotation_cnt = images_annotations_info(mask_path)

    # Save the COCO JSON to a file
    with open(dest_json, "w") as outfile:
        json.dump(coco_format, outfile, sort_keys=True, indent=4)

    print(f"Created {annotation_cnt} annotations for images in folder: {mask_path}")
    

def extract_id_from_path(path: str, dataset_name: str = None):
    if not dataset_name:
        dataset_name = path.split('/')[-3]
    file_name = path.split('/')[-1].split('.')[0]
    return f'{dataset_name}_{file_name}.tif'


def copy_files_with_rename(source_directory: str, destination_directory: str, dataset_name: str = None):
    # Iterate over files in the source directory
    for filename in os.listdir(source_directory):
        # Build the full path for source and destination
        source_path = os.path.join(source_directory, filename)

        # Build the new filename
        new_filename = extract_id_from_path(source_path, dataset_name)

        # Build the full path for the destination
        destination_path = os.path.join(destination_directory, new_filename)

        # Copy the file to the destination with the new name
        shutil.copy(source_path, destination_path)