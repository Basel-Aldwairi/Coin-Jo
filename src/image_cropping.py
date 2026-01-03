# Basel Al-Dwairi - Dataset restructuring, and  image processing

import json
import tqdm
from PIL import Image

# Data paths
unproccessed_data_path = '../Data/raw/Jordan-Coins-Detection-1/'
data_splits = ['train', 'valid', 'test']
annotations_string = '/_annotations.coco.json'
save_path = '../Data/proccessed/'

# Model sizes
cnn_resize = (224, 224)
svm_resize = (64, 64)

# Main Loop - over each split
for data_split in data_splits:
    data_path = unproccessed_data_path + data_split + annotations_string

    # Read JSON annotations
    with open(data_path, 'r') as f:
        data = json.load(f)

    # Images to be processed
    images = data['images']

    # Image annotations
    annotations = data['annotations']

    # Categories (Classes)
    categories = data['categories']
    categories_search = [c['name'] for c in categories]

    # Loop over each annotation (labeled coin)
    for annotation in tqdm.tqdm(annotations,desc= f'{data_split}'):

        # Ids
        image_id = annotation['image_id']
        annotation_id = annotation['id']
        category_id = annotation['category_id']

        # Remove bills
        if category_id in {0, 3, 5, 6, 8, 9}:
            continue

        category_name = categories_search[category_id]

        # Crop coordinates
        x, y, w, h = annotation['bbox']
        bbox = x, y, x + w, y + h

        # Save paths
        image_name = images[image_id]['file_name']
        image_path = unproccessed_data_path + '/' + data_split + '/' + image_name

        # Image processing - crop & resize
        image = Image.open(image_path)
        image_cropped = image.crop(bbox)

        image_resize = image_cropped.resize(cnn_resize)

        # Saving preprocessed image
        image_save_path = save_path + category_name + '/' + str(image_id) + 'img' + '_' +  str(annotation_id) + 'a' + '.jpg'
        image_resize.save(image_save_path)


