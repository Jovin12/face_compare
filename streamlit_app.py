import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image
import tempfile
import os

st.set_page_config(
    page_title="Face Comparison System",
    page_icon="👤",
    layout="wide"
)

def extract_face_from_image(image_path):
    """Extract face from image and return cropped face"""
    try:
        face_objs = DeepFace.extract_faces(
            img_path=image_path,
            detector_backend='opencv'
        )
        
        if len(face_objs) == 0:
            return None
        
        face_pixels = face_objs[0]['face']
        face_img = (face_pixels * 255).astype('uint8')
        face_img = cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR)
        
        # Save to temporary file
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        cv2.imwrite(temp_path.name, face_img)
        
        return temp_path.name
    except Exception as e:
        st.error(f"Error extracting face: {e}")
        return None

def compare_faces(face1_path, face2_path):
    """Compare two face images"""
    try:
        result = DeepFace.verify(
            img1_path=face1_path,
            img2_path=face2_path,
            model_name='VGG-Face',
            detector_backend='opencv'
        )
        
        return {
            'verified': result['verified'],
            'distance': result['distance'],
            'threshold': result.get('threshold', 0.68)
        }
    except Exception as e:
        st.error(f"Face verification failed: {e}")
        return None

def load_image_from_upload(uploaded_file):
    """Load image from uploaded file and save temporarily"""
    if uploaded_file is not None:
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        with open(temp_path.name, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        return temp_path.name
    return None

def capture_webcam_image():
    """Capture image from webcam"""
    # This will be handled by Streamlit's camera_input
    pass

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .result-box {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 2rem;
    }
    .success {
        background-color: #d4edda;
        border: 2px solid #28a745;
        color: #155724;
    }
    .failure {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        color: #721c24;
    }
    .stButton button {
        width: 100%;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>👤 Face Comparison System</h1>
        <p>Compare your face with your driver's license photo</p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'selfie_path' not in st.session_state:
    st.session_state.selfie_path = None
if 'license_path' not in st.session_state:
    st.session_state.license_path = None
if 'cropped_license_path' not in st.session_state:
    st.session_state.cropped_license_path = None
if 'comparison_done' not in st.session_state:
    st.session_state.comparison_done = False

# Create two columns for input methods
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Your Selfie")
    
    input_method = st.radio(
        "Choose input method:",
        ["Upload Photo", "Take Photo with Camera"],
        key="selfie_method"
    )
    
    if input_method == "Upload Photo":
        uploaded_selfie = st.file_uploader(
            "Upload your selfie",
            type=['jpg', 'jpeg', 'png'],
            key="selfie_upload"
        )
        if uploaded_selfie:
            st.session_state.selfie_path = load_image_from_upload(uploaded_selfie)
            if st.session_state.selfie_path:
                st.image(uploaded_selfie, caption="Your Selfie", use_container_width=True)
    
    else:  # Camera input
        camera_selfie = st.camera_input("Take a selfie", key="selfie_camera")
        if camera_selfie:
            st.session_state.selfie_path = load_image_from_upload(camera_selfie)
            if st.session_state.selfie_path:
                st.image(camera_selfie, caption="Your Selfie", use_container_width=True)

with col2:
    st.subheader("🪪 Driver's License")
    
    input_method_license = st.radio(
        "Choose input method:",
        ["Upload Photo", "Take Photo with Camera"],
        key="license_method"
    )
    
    if input_method_license == "Upload Photo":
        uploaded_license = st.file_uploader(
            "Upload driver's license",
            type=['jpg', 'jpeg', 'png'],
            key="license_upload"
        )
        if uploaded_license:
            st.session_state.license_path = load_image_from_upload(uploaded_license)
            if st.session_state.license_path:
                st.image(uploaded_license, caption="Driver's License", use_container_width=True)
    
    else:  # Camera input
        camera_license = st.camera_input("Take photo of license", key="license_camera")
        if camera_license:
            st.session_state.license_path = load_image_from_upload(camera_license)
            if st.session_state.license_path:
                st.image(camera_license, caption="Driver's License", use_container_width=True)

# Process license to extract face
if st.session_state.license_path and not st.session_state.cropped_license_path:
    with st.spinner("Extracting face from driver's license..."):
        cropped_path = extract_face_from_image(st.session_state.license_path)
        if cropped_path:
            st.session_state.cropped_license_path = cropped_path
            st.success("✅ Face detected and extracted from license!")
        else:
            st.error("❌ No face detected on the driver's license. Please try another photo.")

# Compare button
if st.session_state.selfie_path and st.session_state.cropped_license_path:
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Compare Faces", type="primary", use_container_width=True):
            with st.spinner("Comparing faces..."):
                result = compare_faces(
                    st.session_state.selfie_path,
                    st.session_state.cropped_license_path
                )
                
                if result:
                    st.session_state.comparison_done = True
                    st.session_state.result = result
                else:
                    st.error("Comparison failed. Please try again.")
    
    # Show extracted face for debugging
    if st.checkbox("Show extracted face from license"):
        if st.session_state.cropped_license_path:
            st.image(
                st.session_state.cropped_license_path, 
                caption="Extracted Face from License", 
                use_container_width=True
            )

# Display results
if st.session_state.comparison_done and hasattr(st.session_state, 'result'):
    result = st.session_state.result
    
    if result['verified']:
        st.markdown(f"""
            <div class="result-box success">
                <h2>✅ Match Found!</h2>
                <p>The face in your selfie matches the face on the driver's license.</p>
                <p>Confidence: {((1 - result['distance']) * 100):.2f}%</p>
                <p>Distance Score: {result['distance']:.4f}</p>
                <p>Threshold: {result['threshold']:.4f}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="result-box failure">
                <h2>❌ No Match</h2>
                <p>The face in your selfie does NOT match the face on the driver's license.</p>
                <p>Confidence: {((1 - result['distance']) * 100):.2f}%</p>
                <p>Distance Score: {result['distance']:.4f}</p>
                <p>Threshold: {result['threshold']:.4f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Reset button
    if st.button("🔄 Reset All", type="secondary"):
        # Clean up temp files
        for path in [st.session_state.selfie_path, st.session_state.license_path, 
                    st.session_state.cropped_license_path]:
            if path and os.path.exists(path):
                os.unlink(path)
        
        st.session_state.selfie_path = None
        st.session_state.license_path = None
        st.session_state.cropped_license_path = None
        st.session_state.comparison_done = False
        st.rerun()

# Sidebar with instructions
with st.sidebar:
    st.markdown("## 📋 Instructions")
    st.markdown("""
    1. **Upload/Take your selfie** - Clear frontal photo of your face
    2. **Upload/Take driver's license photo** - Ensure the face on license is clearly visible
    3. **Click "Compare Faces"** to verify if they match
    4. View the results with confidence score
    
    ### Tips for best results:
    - Use good lighting
    - Look directly at the camera
    - Make sure your face is clearly visible
    - License photo should be clear and not blurry
    
    ### How it works:
    This app uses DeepFace with VGG-Face model to extract facial features and calculate similarity between the two faces.
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Model Information")
    st.markdown("""
    - **Model:** VGG-Face
    - **Detector:** OpenCV
    - **Similarity threshold:** 0.68
    - Smaller distance = more similar
    """)

# Cleanup on exit
def cleanup_temp_files():
    for path in [st.session_state.selfie_path, st.session_state.license_path, 
                st.session_state.cropped_license_path]:
        if path and os.path.exists(path):
            try:
                os.unlink(path)
            except:
                pass

# Register cleanup
import atexit
atexit.register(cleanup_temp_files)

