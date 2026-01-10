# Basel Al-Dwairi - User Interface

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')

import streamlit as st
import coin_model
from PIL import Image
import cv2
import numpy as np
import requests
from io import BytesIO

# session_state to avoid reloading
if 'model' not in st.session_state:
    st.session_state.model = coin_model.CoinModel()
if 'predictions' not in st.session_state:
    st.session_state.predictions = None
if 'percentage' not in st.session_state:
    st.session_state.percentage = None
if 'image' not in st.session_state:
    st.session_state.image = None
if 'view_predictions' not in st.session_state:
    st.session_state.view_predictions = False
if 'selected_mode' not in st.session_state:
    st.session_state.selected_mode = 'Single Coin'
if 'total_ammount' not in st.session_state:
    st.session_state.total_ammount = None

# Cashe identical prediction request, improves UX
@st.cache_data(show_spinner=True)
def cashed_predict(img, **params):
    st.session_state.model.predict_image(img)

# Don't view preictions if image changed , helps with clarity
st.session_state.view_predictions = False

st.sidebar.title('Options')

# Prediction method
selected_mode = st.sidebar.radio('Prediction Mode', options=['Single Coin', 'Multiple Coins - Segmentation'])
st.session_state.selected_mode = selected_mode

# Choose which images to predict
file_type = st.sidebar.radio('File Type', options=['Local File', 'Web Image'])

# Local file
if file_type == 'Local File':

    img_file = st.file_uploader('Upload a local file image', accept_multiple_files=False)
    if img_file:
        try:
            image_pil = Image.open(img_file)
            image = np.array(image_pil)
            # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            st.session_state.image = image
        except Exception as e:
            st.error('Invalid Image File')

# Web image
if file_type == 'Web Image':

    url = st.text_input('Enter Image URL', value="")
    if url:
        try:

            #
            response = requests.get(url)
            image_pil = Image.open(BytesIO(response.content)).convert('RGB')
            image_cv = np.array(image_pil)
            image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)

            st.session_state.image = image_cv
        except Exception as e:
            st.error('Invalid Image URL')

# Show image toggle
if st.session_state.image is not None:
    show_image = st.toggle('Show Selected Image')
    if show_image:
        st.markdown('''
        ---
        **Image to be Processed:**
        ''')
        image_pil = Image.fromarray(st.session_state.image)
        st.image(image_pil)

# Predict classification
predict_button = st.button('Predict Coin')
if predict_button:
    model = st.session_state.model

    # Single coin predition
    if st.session_state.selected_mode == 'Single Coin':
        predictions =  model.predict_image(st.session_state.image)
        st.session_state.predictions = predictions
        st.session_state.view_predictions = True

    # Segmentation mode
    if st.session_state.selected_mode == 'Multiple Coins - Segmentation':
        predictions = model.predict_segmented_images(st.session_state.image)
        total_ammount = model.predict_total_ammount(predictions)
        st.session_state.total_ammount = total_ammount
        st.session_state.view_predictions = True



# Show prediction replies
if st.session_state.view_predictions:

    # Single coin prediction
    if st.session_state.selected_mode == 'Single Coin':
        predictions = st.session_state.predictions
        predictions.sort(reverse=True)

        confidence, prediction = predictions[0]

        # Show label and confidence percentage
        st.success(f'Prediction: {prediction} ({confidence:.3f}%)')

        # Draw bar chart for predictions
        fig, ax = coin_model.plot_predictions(predictions)

        st.pyplot(fig)

    # Multicoin prediction
    if st.session_state.selected_mode == 'Multiple Coins - Segmentation':

        # Show total sum
        total_ammount = st.session_state.total_ammount
        st.success(f'Total Amount: {total_ammount}')