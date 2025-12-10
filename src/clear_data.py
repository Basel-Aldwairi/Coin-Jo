import os
import glob
import tqdm

folder = '../Data/proccessed'
categories = os.listdir(folder)

for category in tqdm.tqdm(categories, desc='Removing files'):
    category_folder = os.path.join(folder, category)
    category_files = glob.glob(os.path.join(category_folder, '*'))

    for file in category_files:
        os.remove(file)

print('Removed Files!')
