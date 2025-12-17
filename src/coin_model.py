from tensorflow.keras.models import Model,load_model
from PIL import Image
import numpy as np

class CoinModel:

    def __init__(self):
        self.model = load_model('coin_model.keras')
        self.labels = ['0.5 JD', '0.25 JD', '10 Piasters', '5 Piasters']

    def predict_image(self, img_path):
        img = Image.open(img_path)
        img = img.resize((224, 224))

        img_np = np.array(img)
        img_np = img_np.astype('float32')

        img_preprocessed = img_np
        img_preprocessed = np.expand_dims(img_preprocessed, axis=0)

        prediction = self.model.predict(img_preprocessed)[0]

        prediction_labels = list(zip(prediction, self.labels))
        prediction_labels.sort(reverse=True)

        percentage, final_prediction = prediction_labels[0]

        return final_prediction, percentage

