# Basel Al-Dwairi - Model Class

from tensorflow.keras.models import Model,load_model
import numpy as np
from pathlib import Path
import cv2
from matplotlib import pyplot as plt

# Used to graph the results to a bar chart
def plot_predictions(predictions):

    labels = [p[1] for p in predictions]
    values = [round(p[0], 3) for p in predictions]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title('Predictions Chart')
    ax.set_xlabel('Denominations')
    ax.set_ylabel('Prediction Confidence Percentage')

    return fig, ax


# Model interface class
class CoinModel:


    def __init__(self):

        # Load model
        self.ROOT = Path(__file__).parent.parent
        self.keras_file = self.ROOT / 'src' / 'coin_model.keras'

        self.model = load_model(self.keras_file)

        self.labels = ['0.5 JD', '0.25 JD', '10 Piasters', '5 Piasters']

    # Main class method
    def predict_image(self, image):

        # Resize to fit input
        size = (224, 224)
        img_preprocessed = cv2.resize(image, size).astype('float32')

        img_preprocessed = np.expand_dims(img_preprocessed, axis=0)

        # Predict Class
        prediction = self.model.predict(img_preprocessed)[0]

        # Zip prediction labels and perentages in form (percentage, label)
        prediction_labels = list(zip(prediction, self.labels))

        return prediction_labels

