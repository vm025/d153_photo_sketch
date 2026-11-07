import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Photo to Pencil Sketch",
    page_icon="✏️",
    layout="wide"
)

# ----------------------------------------------------
# Custom CSS
# ----------------------------------------------------
st.markdown("""
<style>

.stApp {
    background-color: #f4f6f8;
}

.main-title {
    text-align: center;
    color: #2E4053;
    font-size: 42px;
    font-weight: bold;
}

.sub-title {
    text-align: center;
    color: #566573;
    font-size: 18px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Header
# ----------------------------------------------------
st.markdown(
    '<p class="main-title">✏️ Photo to Pencil Sketch</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Upload a photo and download a beautiful pencil sketch version.</p>',
    unsafe_allow_html=True
)

# ----------------------------------------------------
# Sketch Function
# ----------------------------------------------------
def generate_sketch(image_array, blur_size):

    # Convert to grayscale
    gray_img = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

    # Improve contrast
    gray_img = cv2.equalizeHist(gray_img)

    # Invert image
    inverted = cv2.bitwise_not(gray_img)

    # Blur inverted image
    blur = cv2.GaussianBlur(
        inverted,
        (blur_size, blur_size),
        sigmaX=0
    )

    # Invert blurred image
    inverted_blur = cv2.bitwise_not(blur)

    # Create sketch
    sketch = cv2.divide(
        gray_img,
        inverted_blur,
        scale=256.0
    )

    return sketch


# ----------------------------------------------------
# Sidebar Controls
# ----------------------------------------------------
st.sidebar.header("Settings")

blur_size = st.sidebar.slider(
    "Sketch Intensity",
    min_value=5,
    max_value=51,
    value=21,
    step=2,
    help="Higher value = softer pencil effect"
)

# ----------------------------------------------------
# File Upload
# ----------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Photo",
    type=["jpg", "jpeg", "png"]
)

# ----------------------------------------------------
# Process Image
# ----------------------------------------------------
if uploaded_file is not None:

    try:

        image = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(image)

        sketch = generate_sketch(
            image_np,
            blur_size
        )

        # Display images
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(
                image,
                use_container_width=True
            )

        with col2:
            st.subheader("Sketch Image")
            st.image(
                sketch,
                use_container_width=True
            )

        # Convert sketch to JPEG bytes
        sketch_image = Image.fromarray(sketch)

        buffer = io.BytesIO()

        sketch_image.save(
            buffer,
            format="JPEG",
            quality=100
        )

        jpg_bytes = buffer.getvalue()

        st.divider()

        st.download_button(
            label="📥 Download Sketch JPG",
            data=jpg_bytes,
            file_name="pencil_sketch.jpg",
            mime="image/jpeg",
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Error processing image: {e}")

else:
    st.info("👆 Upload a JPG or PNG image to generate its sketch.")