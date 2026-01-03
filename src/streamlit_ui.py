import streamlit as st
import coin_model
from PIL import Image
import cv2
import numpy as np
import requests
from io import BytesIO

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

@st.cache_data(show_spinner=True)
def cashed_predict(img, **params):
    st.session_state.model.predict_image(img)


st.session_state.view_predictions = False

file_type = st.selectbox('File Type', options=['Local File', 'Web Image'])

if file_type == 'Local File':

    img_file = st.file_uploader('Upload a local file image', accept_multiple_files=False)
    if img_file:
        try:
            image_pil = Image.open(img_file)
            image = np.array(image_pil)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            st.session_state.image = image
        except Exception as e:
            st.error('Invalid Image File')

if file_type == 'Web Image':

    url = st.text_input('Enter Image URL', value="")
    if url:
        try:

            response = requests.get(url)
            image_pil = Image.open(BytesIO(response.content)).convert('RGB')
            image_cv = np.array(image_pil)
            image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)

            st.session_state.image = image_cv
        except Exception as e:
            st.error('Invalid Image URL')


if st.session_state.image is not None:
    show_image = st.toggle('Show Selected Image')
    if show_image:
        st.markdown('''
        ---
        **Image to be Processed:**
        ''')
        image_pil = Image.fromarray(st.session_state.image)
        st.image(image_pil)


predict_button = st.button('Predict Coin')
if predict_button:
    model = st.session_state.model
    # print(st.session_state.image)
    # prediction, percentage =  model.predict_image(st.session_state.image)

    predictions =  model.predict_image(st.session_state.image)
    st.session_state.predictions = predictions
    st.session_state.view_predictions = True

if st.session_state.view_predictions:
    predictions = st.session_state.predictions
    predictions.sort(reverse=True)

    confidence, prediction = predictions[0]

    st.success(f'Prediction: {prediction} ({confidence:.3f}%)')

    fig, ax = coin_model.plot_predictions(predictions)

    st.pyplot(fig)