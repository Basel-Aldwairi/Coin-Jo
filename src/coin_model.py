from tensorflow.keras.models import Model,load_model
from PIL import Image
import numpy as np
from pathlib import Path
import cv2
from matplotlib import pyplot as plt


def plot_predictions(predictions):

    labels = [p[1] for p in predictions]
    values = [round(p[0], 3) for p in predictions]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title('Predictions Chart')
    ax.set_xlabel('Denominations')
    ax.set_ylabel('Prediction Confidence Percentage')

    return fig, ax


class CoinModel:



    def __init__(self):

        self.ROOT = Path(__file__).parent.parent
        self.keras_file = self.ROOT / 'src' / 'coin_model.keras'

        self.model = load_model(self.keras_file)
        self.labels = ['0.5 JD', '0.25 JD', '10 Piasters', '5 Piasters']

    def predict_image(self, image):

        size = (224, 224)
        img_preprocessed = cv2.resize(image, size).astype('float32')

        img_preprocessed = np.expand_dims(img_preprocessed, axis=0)

        prediction = self.model.predict(img_preprocessed)[0]

        prediction_labels = list(zip(prediction, self.labels))
        # prediction_labels.sort(reverse=True)

        # percentage, final_prediction = prediction_labels[0]

        return prediction_labels

