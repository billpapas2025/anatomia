import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance

def apply_contrast(image, level):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(level)

def apply_brightness(image, level):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(level)

def main():
    st.title("Análisis de Imágenes de Modelos 3D")
    st.write("Carga una imagen para analizar.")

    uploaded_file = st.file_uploader("Elige una imagen...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_array = np.array(image)

        st.image(img_array, caption='Imagen original', use_column_width=True)

        option = st.selectbox("Elige una opción de procesamiento:",
                              ("Escala de Grises", "Detección de Bordes", "Filtro de Desenfoque", "Ajuste de Brillo y Contraste"))

        processed_img = None

        if option == "Escala de Grises":
            gray_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            processed_img = gray_image
            st.image(processed_img, caption='Imagen en Escala de Grises', use_column_width=True)

        elif option == "Detección de Bordes":
            gray_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray_image, 100, 200)
            processed_img = edges
            st.image(processed_img, caption='Bordes Detectados', use_column_width=True)

        elif option == "Filtro de Desenfoque":
            blur_radius = st.slider("Elige el radio de desenfoque:", 1, 10, 5)
            blurred_image = cv2.GaussianBlur(img_array, (blur_radius * 2 + 1, blur_radius * 2 + 1), 0)
            processed_img = blurred_image
            st.image(processed_img, caption='Imagen Desenfocada', use_column_width=True)

        elif option == "Ajuste de Brillo y Contraste":
            brightness = st.slider("Ajuste de Brillo", 0.5, 3.0, 1.0)
            contrast = st.slider("Ajuste de Contraste", 0.5, 3.0, 1.0)
            bright_img = apply_brightness(image, brightness)
            contrast_img = apply_contrast(bright_img, contrast)
            processed_img = np.array(contrast_img)
            st.image(processed_img, caption='Brillo y Contraste Ajustados', use_column_width=True)

        if processed_img is not None:
            if st.button('Guardar Imagen Procesada'):
                save_image = Image.fromarray(processed_img)
                save_image.save("processed_image.png")
                st.write("Imagen guardada como `processed_image.png`")

if __name__ == "__main__":
    main()
