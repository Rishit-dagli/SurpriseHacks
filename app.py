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
