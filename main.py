import streamlit as st
import time
import cv2
from PIL import Image
import numpy as np
import io
import base64

st.set_page_config(
    page_title="Konversi Gambar ke Sketsa Pensil",
    initial_sidebar_state="expanded",
)


def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href


def get_sketched_image(img):

    file_bytes = np.asarray(bytearray(img), dtype=np.uint8)
    cvImage = cv2.imdecode(file_bytes, 1)

    cvImageGrayScale = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
    cvImageGrayScaleInversion = 255 - cvImageGrayScale
    cvImageBlured = cv2.GaussianBlur(cvImageGrayScaleInversion, (21, 21), 0)
    sketchImage = cv2.divide(cvImageGrayScale, 255 - cvImageBlured, scale=256)

    return sketchImage


st.title("Konversi Gambar ke Sketsa")

st.sidebar.title("Unggah Gambar")

st.set_option('deprecation.showfileUploaderEncoding', False)

img = Image.open("upload.jpg")
image = st.image(img)

uploaded_file = st.sidebar.file_uploader(" ", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image.image(uploaded_file)

if st.sidebar.button("Mulai Konversi"):

    if uploaded_file is None:
        st.sidebar.error("Upload gambar terlebih dahulu!")

    else:
        with st.spinner('Memulai Konversi...'):

            sketchImage = get_sketched_image(uploaded_file.read())

            time.sleep(2)
            # image.image(sketchImage)
            st.success('Konversi Selesai!')
            st.success(
                'Klik "Download Image" untuk mengunduh sketsa hasil konversi')
            image = st.image(sketchImage)
            # st.sidebar.success("Please scroll down for your sketched image!")


if st.button("Download"):
    if uploaded_file:
        sketchedImage = get_sketched_image(uploaded_file.read())
        image.image(sketchedImage)
        result = Image.fromarray(sketchedImage)
        st.success("Press the below Link")
        st.markdown(get_image_download_link(result, "sketched.jpg",
                                            'Download '+"Sketched.jpg"), unsafe_allow_html=True)
    else:
        st.error("Upload gambar terlebih dahulu!")
