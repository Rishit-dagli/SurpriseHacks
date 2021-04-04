import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
import json


@st.cache
def load_model():
    with open('./models/class_indices.json') as json_file:
        class_indices = json.load(json_file)
    model = tf.keras.models.load_model('./models/plant_disease.h5')
    return model, class_indices


st.title("Plant Disease Recognizer🌱")
st.subheader("A minimalistic web app to identify disease in plant leaves from images")

file = st.file_uploader("Please upload an image file", type=["jpg", "png"])

if file is None:
    st.text("You have not uploaded an image file")
else:
    image = Image.open(file)
    st.image(image, use_column_width='auto')

    image = image.resize((224, 224))
    image = np.expand_dims(np.asarray(image), axis=0) / 255

    model_load_state = st.text('Loading model...')
    model, class_indices = load_model()
    model_load_state.text("Model loaded! (using st.cache)")

    predictions = model(image)

    class_indices = {v: k for (k, v) in class_indices.items()}
    st.subheader("It is a " + class_indices[np.argmax(predictions)])
