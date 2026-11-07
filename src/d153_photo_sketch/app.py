import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(
    page_title="Photo to Pencil Sketch",
    page_icon="✏️",
    layout="wide"
)

# ----------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------
st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7ff;
    }

    .main-title {
        text-align: center;
        color: orangered;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .sub-title {
        text-align: center;
        color: #5d6d7e;
        font-size: 18px;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown(
    '<p class="main-title">✏️ Photo to Pencil Sketch</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Upload a photo, adjust the sketch effect, and download the result.</p>',
    unsafe_allow_html=True
)

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------
st.sidebar.header("Sketch Settings")

blur_size = st.sidebar.slider(
    "Pencil Softness",
    min_value=3,
    max_value=101,
    value=31,
    step=2,
    help="Higher values create softer pencil strokes."
)

sketch_strength = st.sidebar.slider(
    "Sketch Intensity",
    min_value=100,
    max_value=500,
    value=256,
    step=10,
    help="Higher values create darker and stronger sketch effects."
)

# ----------------------------------------------------
# FUNCTION
# ----------------------------------------------------
def generate_sketch(image_array, blur_size, sketch_strength):
    """
    Convert image to pencil sketch.
    """

    # Grayscale
    gray = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2GRAY
    )

    # Enhance contrast
    gray = cv2.equalizeHist(gray)

    # Invert
    inverted = cv2.bitwise_not(gray)

    # Blur
    blur = cv2.GaussianBlur(
        inverted,
        (blur_size, blur_size),
        0
    )

    # Invert blurred image
    inverted_blur = cv2.bitwise_not(blur)

    # Pencil sketch
    sketch = cv2.divide(
        gray,
        inverted_blur,
        scale=sketch_strength
    )

    # Extra contrast adjustment based on intensity slider
    alpha = sketch_strength / 256.0

    sketch = cv2.convertScaleAbs(
        sketch,
        alpha=alpha,
        beta=0
    )

    return sketch


# ----------------------------------------------------
# FILE UPLOAD
# ----------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

# ----------------------------------------------------
# PROCESS IMAGE
# ----------------------------------------------------
if uploaded_file is not None:

    try:

        image = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(image)

        sketch = generate_sketch(
            image_np,
            blur_size,
            sketch_strength
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(
                image,
                width="stretch"
            )

        with col2:
            st.subheader("Sketch Image")
            st.image(
                sketch,
                width="stretch"
            )

        # ----------------------------------------------------
        # DOWNLOAD JPG
        # ----------------------------------------------------
        sketch_pil = Image.fromarray(sketch)

        buffer = io.BytesIO()

        sketch_pil.save(
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
            width="stretch"
        )

    except Exception as e:
        st.error(f"Error processing image: {e}")

else:
    st.info("👆 Upload a JPG or PNG image to begin.")