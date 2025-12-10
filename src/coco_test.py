import json

path = '../Data/raw/Jordan-Coins-Detection-1/test/_annotations.coco.json'

with open(path, 'r') as f:
    data = json.load(f)

