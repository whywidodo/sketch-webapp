import streamlit as st
import time
import cv2
from PIL import Image
import numpy as np
import io
import base64

# Judul Tab
favImage = Image.open("favicon.png")
st.set_page_config(
    page_icon=favImage,
    page_title="Dashboard | Konversi Gambar",
    initial_sidebar_state="collapsed"  # Collapsed, Extended, Auto
)

# Judul pada Bagian Homepage
st.header("Konversi Gambar")

# Menambahkan Judul Unggah Gambar
# di Sebelah Kiri/Sidebar dengan ukuran tulisan subheader
st.sidebar.subheader("Unggah Gambar")
st.set_option('deprecation.showfileUploaderEncoding', False)

# Membuka Gambar Dengan Nama upload.jpg
img = Image.open("upload.jpg")
# Menampilkan Gambar kedalam Homepage
image = st.image(img)
# Membuat Area Untuk Unggah Gambar dengan tipe (png, jpg, jpeg)
# di Sebelah Kiri/Sidebar
upFile = st.sidebar.file_uploader(
    "", type=['png', 'jpg', 'jpeg'],)


def imgDownload(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href


# Perintah Konversi Gambar
def imgKonversi(img):

    file_bytes = np.asarray(bytearray(img), dtype=np.uint8)
    cvImage = cv2.imdecode(file_bytes, 1)

    # Perintah Konversi Default Umumnya
    imgGray = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
    imgInversi = 255 - imgGray
    imgBlur = cv2.GaussianBlur(imgInversi, (21, 21), 0)
    imgSketsa = cv2.divide(imgGray, 255 - imgBlur, scale=256)

    return imgSketsa


# Jika Sudah Ada Gambar yang Diupload
if upFile is not None:
    image.image(upFile)

# Jika Pengguna Menekan Tombol "Mulai Konversi"
if st.sidebar.button("Mulai Konversi"):

    # Jika Pengguna Menekan Tombol "Mulai Konversi"
    # Tapi Belum Ada Gambar yang Diupload
    if upFile is None:
        st.sidebar.error("Upload gambar terlebih dahulu!")

    # Jika Pengguna Menekan Tombol "Mulai Konversi"
    # Dan Sudah Ada Gambar yang Diupload
    else:
        # Memberikan efek spinner (proses berjalan)
        with st.spinner('Memulai Konversi...'):

            imgSketsa = imgKonversi(upFile.read())

            # Waktu untuk delay (detik)
            time.sleep(2)
            st.success('Konversi Selesai!')  # Style teks sukses
            st.success(
                'Klik "Download Image" untuk mengunduh sketsa hasil konversi')

            # Akan menampilkan gambar yang telah dikonversi menjadi sketsa
            image = st.image(imgSketsa)


# Jika Pengguna Menekan Tombol Download
if st.button("Download"):
    if upFile:   # Apabila gambar sudah di upload
        sketchedImage = imgKonversi(upFile.read())
        image.image(sketchedImage)
        result = Image.fromarray(sketchedImage)
        st.success("Tekan Tombol dibawah ini.")
        st.markdown(imgDownload(result, "sketched.jpg",
                                'Download '+"Sketched.jpg"), unsafe_allow_html=True)
    else:   # Apabila gambar belum di upload
        st.error("Upload gambar terlebih dahulu!")

# Pemberian Identitas Kelompok
st.sidebar.subheader("Anggota")
st.sidebar.text('20SA1004 Wahyu Widodo')
st.sidebar.text('20SA1038 Devani Laras Sati')
st.sidebar.text('20SA1115 Taofik Arianto')
st.sidebar.text('20SA1163 Fitroh Izatul Malkiyah')
st.sidebar.text('20SA1280 Akhil Nur Riyadi')
