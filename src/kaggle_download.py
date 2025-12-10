from roboflow import Roboflow
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

rf = Roboflow(api_key=api_key)
project = rf.workspace("german-jordanian-university-hnx6e").project("jordan-coins-detection-nqdbs-2x3fe")
version = project.version(1)
dataset = version.download("coco")
