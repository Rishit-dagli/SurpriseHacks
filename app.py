import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import json


@st.cache
def load_model():
    with open('./models/class_indices.json') as json_file:
        class_indices = json.load(json_file)
    model = tf.keras.models.load_model('./models/plant_disease.h5')
    return model, class_indices

st.write("""
         # Plant Disease Recognizer
         """
         )
st.write("A minimalistic web app to identify disease in plant leaves from images")

file = st.file_uploader("Please upload an image file", type=["jpg", "png"])

if file is None:
    st.text("You have not uploaded an image file")
else:
    image = Image.open(file)
    st.image(image, use_column_width=True)

    image = image.resize((224, 224))
    image = np.expand_dims(np.asarray(image), axis = 0) / 255
    model, class_indices = load_model()
    predictions = model(image)
