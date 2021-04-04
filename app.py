import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
import json

SEEDLING_EMOJI_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/facebook/65/seedling_1f331" \
                    ".png "
page_title = "Plant Diseases"

# Set page title and favicon.
st.set_page_config(
    page_title=page_title, page_icon=SEEDLING_EMOJI_URL,
)


@st.cache
def load_model():
    with open('./models/class_indices.json') as json_file:
        class_indices = json.load(json_file)
    model = tf.keras.models.load_model('./models/plant_disease.h5')
    return model, class_indices

# Display header.
st.markdown("<br>", unsafe_allow_html=True)
st.image(SEEDLING_EMOJI_URL, width=80)

"""
# Plant Disease Recognizer
[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2FRishit-dagli%2FSurpriseHacks)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FRishit-dagli%2FSurpriseHacks)
&nbsp[![GitHub Repo stars](https://img.shields.io/github/stars/Rishit-dagli/SurpriseHacks?style=social)](https://github.com/Rishit-dagli/SurpriseHacks/stargazers)
&nbsp[![GitHub followers](https://img.shields.io/github/followers/Rishit-dagli?label=Follow&style=social)](https://github.com/Rishit-dagli)
&nbsp[![Twitter Follow](https://img.shields.io/twitter/follow/rishit_dagli?style=social)](https://twitter.com/intent/follow?screen_name=rishit_dagli)
"""
st.markdown("<br>", unsafe_allow_html=True)
"""A minimalistic web app to identify disease in plant leaves from images
---
"""

file = st.file_uploader("Please upload an image file", type=["jpg", "png"])

if file is None:
    st.text("You have not uploaded an image file")
else:
    image = Image.open(file)
    st.image(image, use_column_width=True)

    image = image.resize((224, 224))
    image = np.expand_dims(np.asarray(image), axis=0) / 255

    model, class_indices = load_model()
    predictions = model(image)

    class_indices = {v: k for (k, v) in class_indices.items()}
    predicted_label = str(class_indices[np.argmax(predictions)])
    species, disease = predicted_label.split("__")

    st.subheader(f"This leaf is of a {species} plant")
    if disease == "healthy":
        st.subheader("This plant is healthy ✔")
    else:
        disease_name = disease.replace("_", " ")
        st.subheader(f"This plant is suffering from {disease_name}")
