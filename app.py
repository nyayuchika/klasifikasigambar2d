import streamlit as st
import numpy as np
import cv2 as cv
from io import BytesIO
import tensorflow as tf
from PIL import Image
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from tensorflow.keras.applications import ResNet50

###Input Image
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    #ini untuk nampilin gambar, outputnya bytes
    bytes_image = uploaded_file.read() #baca image

    #nampilin gambar
    image = Image.open(BytesIO(bytes_image))
    st.image(image, use_column_width=True)
    image_np = np.asarray(image)
    resized_image = cv.resize(image_np, (200,200))
    resized_image = np.expand_dims(resized_image, axis=-1) #add a new dimension
    resized_image = np.expand_dims(resized_image, axis=0)

    # Loading ResNet50 model
    base_resnet_model = ResNet50(include_top=False,
                    input_shape=(200,200,3),
                    pooling='max',classes=8,
                    weights='imagenet')

    base_resnet_model.trainable = False

    resnet_model = tf.keras.models.Sequential([
        base_resnet_model,
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(8, activation="softmax")
    ])
    resnet_model.load_weights("ResNet50.h5")

    #Proses
    result = resnet_model.predict(resized_image)
    # st.write(result)
    hasil = np.argmax(result)

    if hasil==0:
        st.write("Dadar Gulung")
    elif hasil==1:
        st.write("Kastengel")
    elif hasil==2:
        st.write("Klepon")
    elif hasil==3:
        st.write("Lapis")
    elif hasil==4:
        st.write("Lumpur")
    elif hasil==5:
        st.write("Putri Salju")
    elif hasil==6:
        st.write("Risoles")
    else:
        st.write("Serabi")