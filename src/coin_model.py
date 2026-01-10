# Basel Al-Dwairi - Model Class

import os

import tensorflow as tf

tf.config.set_visible_devices([], 'GPU')
tf.config.optimizer.set_jit(False)

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

# Segmentation, each coin alone
def segment_image(image, min_circularity=0.25):

    # Image is np.array() in rgb
    preprocessed_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Gaussian blur, kernel size = (3,3)
    kernel_width = 3
    preprocessed_image = cv2.GaussianBlur(preprocessed_image,
                                          (kernel_width, kernel_width), 0)

    # Retrive edges, lower threashold = 50, upper threshold = 150
    edges = cv2.Canny(preprocessed_image, 50, 150, apertureSize=3)

    # Morphological closing, kernel = ellipse (5,5), iterations = 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    preprocessed_image = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Contours
    contours, _ = cv2.findContours(preprocessed_image,
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours
    coin_contours = []
    for contour in contours:

        # If area is too small, filter out
        area = cv2.contourArea(contour)
        if area < 500:
            continue

        # If perimeter = 0, filter out
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue

        circularity = (4 * np.pi * area) / perimeter ** 2

        # If circularity of contour is less than the minimum, filter out
        if circularity >= min_circularity:
            # Only coins remain
            coin_contours.append(contour)

    # Crop each coin alone
    segmented_images = []
    for contour in coin_contours:
        x, y, w, h = cv2.boundingRect(contour)

        segmented_images.append(image[y:y + h, x:x + w])

    # Return list of segmented coins
    return segmented_images


# Model interface class
class CoinModel:


    def __init__(self):

        # Load model
        # tf.config.run_functions_eagerly(True)

        self.ROOT = Path(__file__).parent.parent
        self.keras_file = self.ROOT / 'src' / 'coin_model.keras'

        self.model = load_model(self.keras_file)

        self.labels = ['0.5 JD', '0.25 JD', '10 Piasters', '5 Piasters']
        self.coin_value_map = {
            '5 Piasters' : 0.05,
            '10 Piasters' : 0.10,
            '0.25 JD' : 0.25,
            '0.5 JD' : 0.5,
        }

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

    # Predict each coins from a raw image of coins
    def predict_segmented_images(self, image, min_circularity=0.25):
        # Get a list of segmented coins
        segemented_images = segment_image(image, min_circularity)

        # Predict each coin alone
        predictions = []
        for segemented_image in segemented_images:
            prediction = self.predict_image(segemented_image)

            # Apeend prediction to list
            prediction.sort()
            prediction = prediction[::-1]
            predictions.append(prediction[0][1])


        # Return predictions for each coin
        return predictions

    # Lookup function for coin value
    def get_coin_value(self, coin_label):
        return self.coin_value_map[coin_label]

    # Returns total sum of all coins
    def predict_total_ammount(self, coin_predictions):
        predicted_values = list(map(self.get_coin_value, coin_predictions))
        return np.array(predicted_values).sum()