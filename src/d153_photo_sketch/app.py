import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Photo to Sketch",
    page_icon="✏️",
    layout="wide"
)

# --------------------------------------------------
# Optional Styling
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #F7F7F7;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("✏️ Photo to Sketch Converter")
st.write("Upload a photo and download a pencil sketch version.")

# --------------------------------------------------
# Upload Image
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Choose a photo",
    type=["jpg", "jpeg", "png"]
)

# --------------------------------------------------
# Sketch Conversion Function
# --------------------------------------------------
def create_sketch(image_array):

    # Convert RGB to grayscale
    grey_img = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

    # Invert image
    invert = cv2.bitwise_not(grey_img)

    # Blur
    blur = cv2.GaussianBlur(invert, (21, 21), 0)

    # Invert blurred image
    inverted_blur = cv2.bitwise_not(blur)

    # Create sketch
    sketch = cv2.divide(
        grey_img,
        inverted_blur,
        scale=256.0
    )

    return sketch


# --------------------------------------------------
# Process Upload
# --------------------------------------------------
if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    sketch = create_sketch(image_np)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("Sketch")
        st.image(sketch, use_container_width=True)

    # Convert sketch to JPG bytes
    sketch_pil = Image.fromarray(sketch)

    jpg_buffer = io.BytesIO()
    sketch_pil.save(jpg_buffer, format="JPEG")
    jpg_bytes = jpg_buffer.getvalue()

    st.download_button(
        label="📥 Download Sketch JPG",
        data=jpg_bytes,
        file_name="sketch.jpg",
        mime="image/jpeg"
    )