import json
import tqdm
from PIL import Image
from pathlib import Path

unproccessed_data_path = '../Data/raw/Jordan-Coins-Detection-1/'
data_splits = ['train', 'valid', 'test']
annotations_string = '/_annotations.coco.json'


cnn_resize = (224, 224)
svm_resize = (64, 64)

save_path = '../Data/proccessed/'

for data_split in data_splits:
    data_path = unproccessed_data_path + data_split + annotations_string

    with open(data_path, 'r') as f:
        data = json.load(f)


    images = data['images']

    annotations = data['annotations']

    categories = data['categories']

    categories_search = [c['name'] for c in categories]

    for annotation in tqdm.tqdm(annotations,desc= f'{data_split}'):

        image_id = annotation['image_id']
        annotation_id = annotation['id']
        category_id = annotation['category_id']

        if category_id in {0, 3, 5, 6, 8, 9}:
            continue

        category_name = categories_search[category_id]

        x, y, w, h = annotation['bbox']
        bbox = x, y, x + w, y + h

        image_name = images[image_id]['file_name']
        image_path = unproccessed_data_path + '/' + data_split + '/' + image_name

        image = Image.open(image_path)
        image_cropped = image.crop(bbox)

        image_resize = image_cropped.resize(cnn_resize)

        image_save_path = save_path + category_name + '/' + str(image_id) + 'img' + '_' +  str(annotation_id) + 'a' + '.jpg'
        image_resize.save(image_save_path)


