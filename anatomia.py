import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

def apply_contrast(image, level):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(level)

def apply_brightness(image, level):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(level)

def apply_grayscale(image):
    return ImageOps.grayscale(image)

def apply_edge_detection(image):
    image = ImageOps.grayscale(image)
    image = image.filter(ImageFilter.FIND_EDGES)
    return image

def apply_blur(image, radius):
    return image.filter(ImageFilter.GaussianBlur(radius))

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
            processed_img = apply_grayscale(image)
            st.image(processed_img, caption='Imagen en Escala de Grises', use_column_width=True)

        elif option == "Detección de Bordes":
            processed_img = apply_edge_detection(image)
            st.image(processed_img, caption='Bordes Detectados', use_column_width=True)

        elif option == "Filtro de Desenfoque":
            blur_radius = st.slider("Elige el radio de desenfoque:", 1, 10, 5)
            processed_img = apply_blur(image, blur_radius)
            st.image(processed_img, caption='Imagen Desenfocada', use_column_width=True)

        elif option == "Ajuste de Brillo y Contraste":
            brightness = st.slider("Ajuste de Brillo", 0.5, 3.0, 1.0)
            contrast = st.slider("Ajuste de Contraste", 0.5, 3.0, 1.0)
            bright_img = apply_brightness(image, brightness)
            contrast_img = apply_contrast(bright_img, contrast)
            processed_img = contrast_img
            st.image(processed_img, caption='Brillo y Contraste Ajustados', use_column_width=True)

        if processed_img is not None:
            if st.button('Guardar Imagen Procesada'):
                processed_img.save("processed_image.png")
                st.write("Imagen guardada como `processed_image.png`")

if __name__ == "__main__":
    main()
