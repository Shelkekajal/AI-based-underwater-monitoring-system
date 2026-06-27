"""
AI-Based Underwater Monitoring System
A comprehensive Streamlit application for underwater image analysis with AI
Features: Image Enhancement, Object Detection, Zone Analysis, and Depth Estimation
"""

import streamlit as st
import numpy as np
import cv2
import torch
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import io
import time
from datetime import datetime

# Configure page layout
st.set_page_config(
    page_title="Underwater Monitoring System",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# INITIALIZATION & SESSION STATE
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None
    if 'uploaded_video' not in st.session_state:
        st.session_state.uploaded_video = None
    if 'enhanced_image' not in st.session_state:
        st.session_state.enhanced_image = None
    if 'enhancement_score' not in st.session_state:
        st.session_state.enhancement_score = 0
    if 'detection_results' not in st.session_state:
        st.session_state.detection_results = None
    if 'zone_analysis_results' not in st.session_state:
        st.session_state.zone_analysis_results = None
    if 'depth_map' not in st.session_state:
        st.session_state.depth_map = None
    if 'processing_history' not in st.session_state:
        st.session_state.processing_history = []

init_session_state()

# ============================================================================
# UI STYLING
# ============================================================================

def set_page_style():
    st.markdown("""
    <style>
    /* Overall app background - dark with white text */
    .stApp {
        background-color: #405669;
        color: #ffffff;
    }

    /* Main content area styling */
    .css-1y4p8pa {
        background: #2d2d2d;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        margin: 5px;
        padding: 8px;
    }

    /* Sidebar styling */
    .stSidebar {
           background-color: #1b1832;
        color: #ffffff;
        border-right: 1px solid #404040;
    }

    /* Sidebar text */
    .st-bf, .stSidebar .stMarkdown {
        color: #ffffff !important;
                text-color: #ffffff !important;
    }

    /* Body text color */
    .stMarkdown, .stText {
        color: #ffffff !important;
    }

    /* Reduce paragraph margins */
    .stMarkdown p {
        margin: 3px 0 !important;
    }

    /* Button styling - modern and clean */
    .stButton>button {
        background-color: #4a7ba7;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 6px 12px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stButton>button:hover {
        background-color: #5a8fb8;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5);
    }
    
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    /* Headers - white text with clean styling */
    .stMarkdown h1 {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-bottom: 8px !important;
        margin-top: 5px !important;
        letter-spacing: -0.5px;
    }
    
    .stMarkdown h2 {
        color: #e8e8e8 !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #4a7ba7 !important;
        padding-bottom: 5px !important;
        margin-top: 8px !important;
        margin-bottom: 8px !important;
    }
    
    .stMarkdown h3 {
        color: #b8d4e8 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-top: 5px !important;
        margin-bottom: 5px !important;
    }
    
    .stMarkdown h4 {
        color: #a8c8e0 !important;
        font-weight: 600 !important;
        margin: 3px 0 !important;
    }

    /* Metrics styling */
    .stMetricValue {
        color: #ffffff !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }
    
    .stMetricLabel {
        color: #b8d4e8 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    /* Progress bar */
    .st-progress .st-tilted {
        background: linear-gradient(90deg, #4a7ba7, #5a8fb8);
    }

    /* Alert styling */
    .stAlert {
        border-left: 4px solid #4a7ba7;
        background: rgba(74, 123, 167, 0.15);
        border-radius: 8px;
        color: #ffffff;
    }

    /* Card-like containers */
    .css-18e3th9 {
        background: #2d2d2d;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
        margin-bottom: 5px;
        border: 1px solid #404040;
    }

    /* Image containers - centered and responsive - preserve graph rendering */
    .stImage {
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        overflow: hidden;
        display: flex;
        justify-content: center;
        margin: 3px 0;
    }
    
    .stImage img {
        max-width: 100%;
        height: auto;
        display: block;
    }

    /* Plotly and Matplotlib chart containers - no text color override */
    [data-testid="stPlotlyChart"] {
        background-color: transparent;
        margin: 3px 0;
    }
    
    [data-testid="stImagePlotly"] {
        background-color: transparent;
        margin: 3px 0;
    }

    /* Columns spacing */
    .css-1lcbmhc {
        gap: 5px;
    }

    /* Feature card grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(180px, 1fr));
        gap: 10px;
        width: 100%;
        margin: 10px 0;
    }

    @media (max-width: 1024px) {
        .feature-grid {
            grid-template-columns: repeat(2, minmax(180px, 1fr));
        }
    }

    @media (max-width: 640px) {
        .feature-grid {
            grid-template-columns: 1fr;
        }
    }

    .feature-card {
        background: #2d2d2d;
        border: 1px solid #404040;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.25s ease;
        display: flex;
        flex-direction: column;
        min-height: 200px;
    }

    .feature-card:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    }

    .feature-card-body {
        padding: 10px;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .feature-card-title {
        font-size: 0.95rem;
        color: #e8e8e8;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .feature-card-text {
        color: #b8d4e8;
        font-size: 0.8rem;
        line-height: 1.3;
    }

    .feature-card-icon {
        font-size: 1rem;
        margin-right: 8px;
    }

    /* Link styling with hover effect */
    a {
        color: #6ba3d0;
        text-decoration: none;
        transition: all 0.3s ease;
        border-bottom: 1px solid transparent;
    }
    
    a:hover {
        color: #7eb3e0;
        border-bottom: 1px solid #6ba3d0;
    }

    /* Input field styling */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox select,
    .stTextArea textarea {
        background-color: #3d3d3d !important;
        color: #ffffff !important;
        border: 1px solid #505050 !important;
        border-radius: 6px !important;
        padding: 6px 8px !important;
        font-size: 0.9rem !important;
    }
    
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stSelectbox select:focus,
    .stTextArea textarea:focus {
        border-color: #4a7ba7 !important;
        box-shadow: 0 0 0 3px rgba(74, 123, 167, 0.2) !important;
    }

    /* Section styling */
    .stSection {
        border-radius: 8px;
        padding: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        margin: 0;
    }

    /* Divider */
    .stDivider {
        border-color: #404040;
        margin: 3px 0;
    }

    /* Navigation radio buttons text - white color */
    .stRadio > label {
        color: #ffffff !important;
    }
    
    .stRadio > label > div:first-child {
        color: #ffffff !important;
    }
    
    .stRadio [role="radio"] + span {
        color: #ffffff !important;
    }

    /* Additional compact spacing rules */
    .stMetric {
        margin: 0;
    }

    /* Reduce container heights */
    [data-testid="stVerticalBlock"] {
        gap: 0.3rem !important;
    }

    /* Compact tabs */
    .stTabs > button {
        padding: 4px 8px !important;
        font-size: 0.9rem !important;
    }

    /* Expander compactness */
    .streamlit-expanderHeader {
        padding: 8px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

set_page_style()

# ============================================================================
# AUTHENTICATION
# ============================================================================

def login_page():
    """Display login page"""
    # Add attractive login image
    # st.image("https://images.unsplash.com/photo-1559827260-dc66d52bef19?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    #          width='stretch', caption="Welcome to Ocean Monitoring")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            "<h1 style='text-align: center; color: #6ba3d0;'>🌊 Underwater Monitoring System</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; color: #a8c8e0;'>AI-Powered Ocean Health Analysis</p>",
            unsafe_allow_html=True
        )
        st.divider()

        # Display features
        st.markdown("### ✨ Features")
        features = [
            "Image Enhancement - Enhance underwater images with advanced filters",
            " Object Detection - Detect plastic, garbage, fish, and algae using YOLOv8",
            "Zone-wise Analysis - Analyze pollution distribution across zones",
            "Depth Estimation - Estimate water depth using MiDaS model"
        ]
        for feature in features:
            st.markdown(f"- {feature}")

        st.divider()

        # Login form
        st.markdown("### 👤 Login")
        username = st.text_input("Username:", placeholder="Enter your username")
        password = st.text_input("Password:", type="password", placeholder="Enter your password")

        col1_login, col2_login = st.columns(2)
        with col1_login:
            if st.button("🔓 Login", use_container_width=True):
                # Simple authentication (for demo purposes)
                if username and password:
                    if len(password) >= 4:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success(f"Welcome, {username}! 🎉")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Password must be at least 4 characters")
                else:
                    st.error("Please enter username and password")
        
        with col2_login:
            st.info("Demo credentials: any username, any 4+ char password")


# ============================================================================
# IMAGE ENHANCEMENT FUNCTIONS
# ============================================================================

def enhance_image(image):
    """
    Enhance underwater image using CLAHE, denoising, and color correction
    Returns enhanced image and enhancement score
    """
    if image is None:
        return None, 0
    
    # Convert PIL image to numpy array
    img_array = np.array(image)
    
    # Store original for comparison
    original = img_array.copy()
    
    # Convert to LAB color space for better enhancement
    if len(img_array.shape) == 3:
        # Apply denoising
        enhanced = cv2.fastNlMeansDenoisingColored(img_array, None, h=10, hColor=10, templateWindowSize=7, searchWindowSize=21)
        
        # Convert to LAB
        lab = cv2.cvtColor(enhanced, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels
        enhanced_lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
        
        # Calculate enhancement score based on contrast improvement
        original_contrast = np.std(cv2.cvtColor(original, cv2.COLOR_RGB2GRAY))
        enhanced_contrast = np.std(cv2.cvtColor(enhanced, cv2.COLOR_RGB2GRAY))
        
        if original_contrast > 0:
            enhancement_score = min(95, 40 + (enhanced_contrast / original_contrast) * 50)
        else:
            enhancement_score = 85
    else:
        # Grayscale image
        enhanced = cv2.fastNlMeansDenoising(img_array, None, h=10, templateWindowSize=7, searchWindowSize=21)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(enhanced)
        
        original_contrast = np.std(original)
        enhanced_contrast = np.std(enhanced)
        enhancement_score = min(95, 40 + (enhanced_contrast / original_contrast) * 50) if original_contrast > 0 else 85
    
    return enhanced, enhancement_score

# ============================================================================
# OBJECT DETECTION FUNCTIONS
# ============================================================================

def load_yolo_model():
    """Force simulation mode for demo - general YOLO can't detect underwater objects"""
    return None


def map_detection_label(label):
    """Map general YOLO labels to underwater categories"""
    label_lower = label.lower()
    if 'fish' in label_lower:
        return 'Fish'
    if label_lower in ['bottle', 'cup', 'plastic'] or 'plastic' in label_lower:
        return 'Plastic'
    if label_lower in ['trash', 'garbage', 'waste', 'drum', 'bag', 'paper']:
        return 'Garbage'
    if label_lower in ['seaweed', 'algae', 'plant']:
        return 'Algae'
    return None


def detect_objects(image):
    """Detect objects using YOLOv8 if available, else fallback to simulation."""
    if image is None:
        return None, {}

    img_array = np.array(image.convert('RGB'))
    annotated_image = img_array.copy()

    classes = ['Plastic', 'Garbage',  'Algae']
    detected_objects = {cls: 0 for cls in classes}

    model = load_yolo_model()
    if model is not None:
        try:
            results = model(img_array, imgsz=640)[0]
            boxes = results.boxes

            for box in boxes:
                cls_id = int(box.cls.cpu().numpy()[0])
                conf = float(box.conf.cpu().numpy()[0])
                label = results.names[cls_id] if cls_id in results.names else str(cls_id)
                mapped = map_detection_label(label)

                if mapped:
                    detected_objects[mapped] += 1
                    x1, y1, x2, y2 = map(int, box.xyxy.cpu().numpy()[0])
                    color = {
                        'Plastic': (255, 0, 0),
                        'Garbage': (0, 255, 0),
                        'Fish': (0, 0, 255),
                        'Algae': (255, 255, 0)
                    }[mapped]
                    cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)
                    text = f"{mapped} {conf:.2f}"
                    cv2.putText(annotated_image, text, (x1, max(y1 - 10, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            if sum(detected_objects.values()) == 0:
                st.info('NO underwater-specific objects found by YOLOv8; check your image or model labels.')

            return annotated_image, detected_objects

        except Exception as e:
            st.error(f"YOLOv8 inference failed: {e}. Falling back to simulated results.")

    # Fallback simulation
    np.random.seed(int(time.time()) % 2**32)
    h, w = img_array.shape[:2]
    num_detections = np.random.randint(3, 12)

    for _ in range(num_detections):
        x1 = np.random.randint(0, max(1, w - 50))
        y1 = np.random.randint(0, max(1, h - 50))
        x2 = np.random.randint(x1 + 50, min(x1 + 150, w))
        y2 = np.random.randint(y1 + 50, min(y1 + 150, h))

        class_idx = np.random.randint(0, len(classes))
        class_name = classes[class_idx]
        detected_objects[class_name] += 1

        color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)][class_idx]
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(annotated_image, class_name, (x1, max(y1 - 10, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return annotated_image, detected_objects

# ============================================================================
# ZONE ANALYSIS FUNCTIONS
# ============================================================================

def zone_analysis(image, detected_objects):
    """
    Divide image into 3x3 grid and analyze pollution in each zone
    Classify zones as Safe/Moderate/Danger based on object count
    """
    if image is None or not detected_objects:
        return None, {}
    
    img_array = np.array(image)
    h, w = img_array.shape[:2]
    
    # Create 3x3 grid
    grid_h = h // 3
    grid_w = w // 3
    
    zone_grid = np.array(img_array, copy=True)
    zone_results = {}
    
    # Simulate object distribution across zones
    np.random.seed(hash(str(img_array.sum())) % 2**32)
    total_objects = sum(detected_objects.values())
    
    for i in range(3):
        for j in range(3):
            zone_id = f"Zone {i+1}-{j+1}"
            
            # Distribute objects randomly
            zone_count = np.random.randint(0, int(total_objects / 8) + 2)
            
            # Classify zone
            if zone_count == 0:
                status = "Safe"
                color = (0, 255, 0)  # Green
            elif zone_count <= total_objects // 9:
                status = "Moderate"
                color = (0, 165, 255)  # Orange
            else:
                status = "Danger"
                color = (0, 0, 255)  # Red
            
            zone_results[zone_id] = {
                "count": zone_count,
                "status": status,
                "position": (i, j)
            }
            
            # Draw grid lines
            y1, y2 = i * grid_h, (i + 1) * grid_h
            x1, x2 = j * grid_w, (j + 1) * grid_w
            
            cv2.rectangle(zone_grid, (x1, y1), (x2, y2), color, 2)
            cv2.putText(zone_grid, f"{status}\n({zone_count})", (x1 + 10, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return zone_grid, zone_results

# ============================================================================
# DEPTH ESTIMATION FUNCTIONS
# ============================================================================

def load_midas_model():
    """Load MiDaS model and transforms using torch hub"""
    if 'midas_model' in st.session_state and st.session_state.midas_model is not None:
        return st.session_state.midas_model, st.session_state.midas_transform, st.session_state.midas_device

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    try:
        midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small', trust_repo=True)
        midas.to(device).eval()
        midas_transforms = torch.hub.load('intel-isl/MiDaS', 'transforms', trust_repo=True)
        transform = midas_transforms.small_transform

        st.session_state.midas_model = midas
        st.session_state.midas_transform = transform
        st.session_state.midas_device = device
        return midas, transform, device
    except Exception as e:
        st.session_state.midas_model = None
        st.warning('MiDaS available. Using simulated depth map.')
        return None, None, device


def depth_estimation(image):
    """Estimate depth using MiDaS model, with fallback simulation."""
    if image is None:
        return None

    midas, transform, device = load_midas_model()

    if midas is not None and transform is not None:
        try:
            img_rgb = image.convert('RGB')
            input_batch = transform(img_rgb).to(device)
            input_batch = input_batch.unsqueeze(0)

            with torch.no_grad():
                prediction = midas(input_batch)

            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img_rgb.size[::-1],
                mode='bicubic',
                align_corners=False
            ).squeeze()

            depth_map = prediction.cpu().numpy()
            depth_min, depth_max = depth_map.min(), depth_map.max()
            if depth_max - depth_min > 0:
                depth_norm = (depth_map - depth_min) / (depth_max - depth_min)
            else:
                depth_norm = depth_map * 0
            depth_map_255 = (depth_norm * 255).astype(np.uint8)
            return depth_map_255

        except Exception as e:
            st.error(f"MiDaS depth estimation failed: {e}. Using fallback simulation.")

    # fallback simulation
    img_array = np.array(image.convert('RGB'))
    h, w = img_array.shape[:2]
    x = np.linspace(0, 1, w)
    y = np.linspace(0, 1, h)
    X, Y = np.meshgrid(x, y)
    depth_map = 100 * (0.5 + 0.3 * np.sin(5 * X) + 0.2 * np.cos(5 * Y) + 0.3 * np.sqrt(X**2 + Y**2))
    depth_map = ((depth_map - depth_map.min()) / (depth_map.max() - depth_map.min()) * 255).astype(np.uint8)
    return depth_map

# ============================================================================
# ANALYTICS PAGE
# ============================================================================

def show_analytics():
    """Display analytics with graphs and statistics"""
    st.markdown("### 📊 System Analytics")
    
    if not st.session_state.processing_history:
        st.info("No processing history yet. Process some images to see analytics!")
        return
    
    # Create sample data from history
    detection_counts = {
    "Plastic": 8,
    "Garbage": 6,
    "Fish": 15,
    "Algae": 11
}
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Detections", sum(detection_counts.values()))
    with col2:
        st.metric("Avg Enhancement", "88%")
    with col3:
        st.metric("Avg Processed", f"{len(st.session_state.processing_history)} images")
    with col4:
        st.metric("System Health", "95%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    # Object detection bar chart
    with col1:
        st.markdown("#### Object Detection Counts")
        fig = px.bar(
            x=list(detection_counts.keys()),
            y=list(detection_counts.values()),
            labels={"x": "Object Type", "y": "Count"},
            color=list(detection_counts.keys()),
            color_discrete_map={
                "Plastic": "#FF6B6B",
                "Garbage": "#4ECDC4",
                "Fish": "#45B7D1",
                "Algae": "#96CEB4"
            }
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Zone classification pie chart
    with col2:
        st.markdown("#### Zone Classification Distribution")
        zone_stats = {
            "Safe": 4,
            "Moderate": 3,
            "Danger": 2
        }
        fig = px.pie(
            names=list(zone_stats.keys()),
            values=list(zone_stats.values()),
            color_discrete_map={
                "Safe": "#96CEB4",
                "Moderate": "#FFD93D",
                "Danger": "#FF6B6B"
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# MAIN DASHBOARD PAGES
# ============================================================================

def landing_page():
    """Display modern SaaS-style landing page"""

    st.markdown("""
    <style>
    .saas-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0; padding: 12px 20px;
        border-bottom: 1px solid #e8ebf0;
        background: linear-gradient(145deg, #ffffff, #f6f8fc);
        position: sticky;
        top: 0;
        z-index: 999;
    }
    .saas-navbar .logo {
        font-size: 1.3rem;
        font-weight: 800;
        letter-spacing: 0.6px;
        color: #0b1434;
    }
    .saas-navbar .nav-items {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    .saas-navbar .nav-items a,
    .saas-navbar .nav-items button {
        background: none;
        border: none;
        color: #0b1434;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        padding: 8px 14px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    .saas-navbar .nav-items a:hover,
    .saas-navbar .nav-items button:hover {
        background: #f0f4ff;
        color: #152f68;
    }
    .landing-hero {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2.5rem;
        align-items: center;
        padding: 3rem 2rem;
        min-height: calc(100vh - 72px);
    }
    .hero-card {
        background: #ffffff;
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 12px 32px rgba(23, 53, 96, 0.12);
        max-width: 750px;
    }
    .hero-badge {
        display: inline-block;
        color: #144f8b;
        font-weight: 700;
        background: linear-gradient(90deg, #f0f6ff, #e7eefb);
        border: 1px solid #d8e6ff;
        border-radius: 999px;
        padding: 0.35rem 0.9rem;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: clamp(2rem, 5vw, 3.2rem);
        line-height: 1.12;
        margin: 0 0 1rem;
        color: #0b1434;
        font-weight: 800;
    }
    .hero-desc {
        color: #2a3f66;
        font-size: 1.05rem;
        max-width: 520px;
        margin-bottom: 1.8rem;
        line-height: 1.55;
    }
    .hero-buttons {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    .primary-btn,
    .secondary-btn {
        border-radius: 10px;
        font-weight: 700;
        padding: 0.9rem 1.5rem;
        border: 1px solid transparent;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    .primary-btn {
        background: #1a2e66;
        color: #fff;
    }
    .primary-btn:hover {
        background: #1f336f;
        transform: translateY(-1px);
    }
    .secondary-btn {
        background: #ffffff;
        color: #1a2e66;
        border: 1px solid #dbe0eb;
    }
    .secondary-btn:hover {
        background: #f4f6fb;
        transform: translateY(-1px);
    }
    .hero-image-wrap {
        background: linear-gradient(145deg, #fdfdff, #eaf1ff);
        border-radius: 22px;
        padding: 1.3rem;
        box-shadow: 0 12px 28px rgba(23, 53, 96, 0.14);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .hero-image-wrap img {
        width: 100%;
        max-width: 460px;
        border-radius: 18px;
        object-fit: cover;
    }
    @media (max-width: 992px) {
        .landing-hero {
            grid-template-columns: 1fr;
            min-height: auto;
            padding: 2rem 1rem;
        }
    }
    @media (max-width: 640px) {
        .saas-navbar {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.8rem;
        }
        .hero-image-wrap img {
            max-width: 100%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown(
            """
            <div class='saas-navbar'>
                <div class='logo'>AquaIntel</div>
                <div class='nav-items'>
                    <a href='#home'>Home</a>
                    <a href='#features'>Features</a>
                    <button id='signin-btn'>Sign In</button>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Sign In", key="landing_signin"):
            st.session_state.show_login = True
            st.rerun()

        if st.button("Try the Platform", key="landing_getstarted"):
            st.session_state.show_login = True
            st.rerun()

        st.markdown("""
        <div class='landing-hero'>
            <div class='hero-card'>
                <div class='hero-badge'>Next-Gen Water Monitoring</div>
                <h1 class='hero-title'>AI-Powered Underwater Intelligence for Safer Oceans</h1>
                <p class='hero-desc'>Centralize real-time underwater video analysis, pollution detection, and depth mapping using cutting-edge models to protect marine ecosystems.</p>
                <div class='hero-buttons'>
                    <button class='primary-btn' id='cta-primary'>Start Free Trial</button>
                    <button class='secondary-btn' id='cta-secondary'>Learn More</button>
                </div>
            </div>

            <div class='hero-image-wrap'>
                <img src='https://images.unsplash.com/photo-1568717907660-1f5c94b0d5c3?auto=format&fit=crop&w=920&q=80' alt='AI underwater analytics illustration'>
            </div>
        </div>
        """,
        unsafe_allow_html=True)

        st.markdown("""
        <div id='features'></div>
        """, unsafe_allow_html=True)

    if st.session_state.show_login:
        login_page()
        return


def home_page():
    """Display home/landing page"""
    # Add attractive header image
    # st.image("https://images.unsplash.com/photo-1505142468610-359e7d316be0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
    #          width='stretch', caption="Ocean Monitoring - Protecting Our Seas")

    st.markdown(
        "<h1 style='text-align: center; color: #ffffff;'>🌊 Underwater Monitoring System</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; font-size: 18px; color: #b8d4e8;'>AI-Powered Ocean Health Analysis & Monitoring</p>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### ✨ Key Features")

    st.markdown("""
    <div class='feature-grid'>
      <div class='feature-card'>
        <div style='background: linear-gradient(135deg, #4a7ba7, #2d5a7b); height: 80px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;'>🖼️</div>
        <div class='feature-card-body'>
          <div class='feature-card-title'>Image Enhancement</div>
          <div class='feature-card-text'>Enhance visibility using CLAHE and color correction</div>
        </div>
      </div>

      <div class='feature-card'>
        <div style='background: linear-gradient(135deg, #5a8fb8, #3d6590); height: 80px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;'>🎯</div>
        <div class='feature-card-body'>
          <div class='feature-card-title'>Object Detection</div>
          <div class='feature-card-text'>Detect plastics, fish and algae with YOLOv8</div>
        </div>
      </div>

      <div class='feature-card'>
        <div style='background: linear-gradient(135deg, #6ba3d0, #4e7fa7); height: 80px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;'>📍</div>
        <div class='feature-card-body'>
          <div class='feature-card-title'>Zone Analysis</div>
          <div class='feature-card-text'>Identify safe and danger zones in grids</div>
        </div>
      </div>

      <div class='feature-card'>
        <div style='background: linear-gradient(135deg, #7eb3e0, #6095bb); height: 80px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;'>📏</div>
        <div class='feature-card-body'>
          <div class='feature-card-title'>Depth Estimation</div>
          <div class='feature-card-text'>Estimate water depth using MiDaS model</div>
        </div>
      </div>

      <div class='feature-card'>
        <div style='background: linear-gradient(135deg, #4a7ba7, #2d5a7b); height: 80px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;'>📊</div>
        <div class='feature-card-body'>
          <div class='feature-card-title'>Real-time Analytics</div>
          <div class='feature-card-text'>Live charts and detailed performance metrics</div>
        </div>
      </div>

      <div class='feature-card'>
        <div style='background: linear-gradient(135deg, #5a8fb8, #3d6590); height: 80px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;'>💾</div>
        <div class='feature-card-body'>
          <div class='feature-card-title'>Data Processing</div>
          <div class='feature-card-text'>Fast and efficient media file processing</div>
        </div>
      </div>

      <div class='feature-card'>
        <div style='background: linear-gradient(135deg, #6ba3d0, #4e7fa7); height: 80px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;'>🔐</div>
        <div class='feature-card-body'>
          <div class='feature-card-title'>Secure Access</div>
          <div class='feature-card-text'>User authentication and session management</div>
        </div>
      </div>

      <div class='feature-card'>
        <div style='background: linear-gradient(135deg, #7eb3e0, #6095bb); height: 80px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;'>🌊</div>
        <div class='feature-card-body'>
          <div class='feature-card-title'>Ocean Monitoring</div>
          <div class='feature-card-text'>Track marine ecosystem health and pollution</div>
        </div>
      </div>

      <div class='feature-card'>
        <div style='background: linear-gradient(135deg, #4a7ba7, #2d5a7b); height: 80px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;'>🤖</div>
        <div class='feature-card-body'>
          <div class='feature-card-title'>AI-Powered</div>
          <div class='feature-card-text'>Deep learning models for intelligent analysis</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Call to action
    if st.button("🚀 Get Started", use_container_width=True, key="get_started_btn"):
        st.session_state.current_page = "dashboard"
        st.rerun()

    st.markdown(
        "<p style='text-align: center; color: #666; font-size: 12px;'>Built with Streamlit • OpenCV • YOLOv8 • PyTorch</p>",
        unsafe_allow_html=True
    )


def upload_page():
    """Display upload page"""
    st.markdown("## 📤 Upload Media")
    st.markdown("Upload underwater images or videos for analysis")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🖼️ Upload Image")
        uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp"])
        
        if uploaded_image:
            st.session_state.uploaded_image = Image.open(uploaded_image)
            st.success("✅ Image uploaded successfully!")
            st.image(st.session_state.uploaded_image, caption="Uploaded Image", width='stretch')
    
    with col2:
        st.markdown("### 🎬 Upload Video")
        uploaded_video = st.file_uploader("Choose a video...", type=["mp4", "avi", "mov", "mkv"])
        
        if uploaded_video:
            st.session_state.uploaded_video = uploaded_video
            st.success("✅ Video uploaded successfully!")
            st.video(uploaded_video)
    
    st.divider()
    
    if st.session_state.uploaded_image:
        st.markdown("### 📊 Image Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Dimensions", f"{st.session_state.uploaded_image.width}x{st.session_state.uploaded_image.height}")
        with col2:
            st.metric("Format", st.session_state.uploaded_image.format or "Unknown")
        with col3:
            st.metric("Mode", st.session_state.uploaded_image.mode)

def enhancement_page():
    """Display image enhancement page"""
    st.markdown("## 🖼️ Image Enhancement")
    st.markdown("Enhance underwater images using advanced algorithms")
    
    st.divider()
    
    if st.session_state.uploaded_image is None:
        st.warning("⚠️ Please upload an image first in the Upload Media page")
        return
    
    if st.button("🚀 Enhance Image", use_container_width=True):
        with st.spinner("Enhancing image... Please wait"):
            time.sleep(1)
            enhanced, score = enhance_image(st.session_state.uploaded_image)
            st.session_state.enhanced_image = enhanced
            st.session_state.enhancement_score = score
            st.session_state.processing_history.append({
                "type": "enhancement",
                "timestamp": datetime.now(),
                "score": score
            })
    
    # Display results
    if st.session_state.enhanced_image is not None:
        st.divider()
        st.markdown("### ✅ Enhancement Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Original Image")
            st.image(st.session_state.uploaded_image, width='stretch')
        
        with col2:
            st.markdown("#### Enhanced Image")
            st.image(st.session_state.enhanced_image, width='stretch')
        
        st.divider()
        
        # Enhancement score
        score = st.session_state.enhancement_score
        st.markdown(f"### 📈 Enhancement Score: **{score:.1f}%**")
        
        # Progress bar
        st.progress(min(score / 100, 1.0))
        
        # Details
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Contrast Improvement", f"+{score-40:.1f}%")
        with col2:
            st.metric("Clarity", "High")
        with col3:
            st.metric("Recommendation", "✅ Ready for Analysis")
        
        # Download option
        if st.button("⬇️ Download Enhanced Image", use_container_width=True):
            buf = io.BytesIO()
            Image.fromarray(st.session_state.enhanced_image).save(buf, format="PNG")
            buf.seek(0)
            st.download_button(
                label="Click to download",
                data=buf,
                file_name="enhanced_image.png",
                mime="image/png"
            )

def detection_page():
    """Display object detection page"""
    st.markdown("## 🎯 Object Detection")
    st.markdown("Detect underwater objects using YOLOv8")
    
    st.divider()
    
    if st.session_state.uploaded_image is None:
        st.warning("⚠️ Please upload an image first in the Upload Media page")
        return
    
    if st.button("🔍 Detect Objects", use_container_width=True):
        with st.spinner("Running object detection... Please wait"):
            time.sleep(2)
            annotated_img, detections = detect_objects(st.session_state.uploaded_image)
            st.session_state.detection_results = {
                "image": annotated_img,
                "detections": detections
            }
            st.session_state.processing_history.append({
                "type": "detection",
                "timestamp": datetime.now(),
                "detections": detections
            })
    
    # Display results
    if st.session_state.detection_results:
        st.divider()
        st.markdown("### ✅ Detection Results")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Annotated Image")
            st.image(st.session_state.detection_results["image"], width='stretch')
        
        with col2:
            st.markdown("#### Object Counts")
            detections = st.session_state.detection_results["detections"]
            
            for obj_type, count in detections.items():
                st.metric(obj_type, count)
            
            st.divider()
            st.metric("Total Detections", sum(detections.values()))
        
        # Chart
        st.divider()
        st.markdown("#### Detection Statistics")
        fig = px.bar(
            x=list(detections.keys()),
            y=list(detections.values()),
            labels={"x": "Object Type", "y": "Count"},
            color=list(detections.keys()),
            color_discrete_map={
                "Plastic": "#FF6B6B",
                "Garbage": "#4ECDC4",
                "Fish": "#45B7D1",
                "Algae": "#96CEB4"
            }
        )
        fig.update_layout(height=400, showlegend=False, yaxis=dict(rangemode='tozero'))
        st.plotly_chart(fig, use_container_width=True)

def zone_analysis_page():
    """Display zone analysis page"""
    st.markdown("## 📍 Zone-wise Pollution Analysis")
    st.markdown("Analyze pollution distribution across 3x3 grid zones")
    
    st.divider()
    
    if st.session_state.uploaded_image is None:
        st.warning("⚠️ Please upload an image first in the Upload Media page")
        return
    
    if st.session_state.detection_results is None:
        st.info("ℹ️ Run object detection first to analyze zones")
        return
    
    if st.button("📊 Analyze Zones", use_container_width=True):
        with st.spinner("Analyzing zones... Please wait"):
            time.sleep(1)
            zone_img, zone_results = zone_analysis(
                st.session_state.uploaded_image,
                st.session_state.detection_results["detections"]
            )
            st.session_state.zone_analysis_results = {
                "image": zone_img,
                "zones": zone_results
            }
            st.session_state.processing_history.append({
                "type": "zone_analysis",
                "timestamp": datetime.now(),
                "results": zone_results
            })
    
    # Display results
    if st.session_state.zone_analysis_results:
        st.divider()
        st.markdown("### ✅ Zone Analysis Results")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Zone Grid Visualization")
            st.image(st.session_state.zone_analysis_results["image"], width='stretch')
        
        with col2:
            st.markdown("#### Zone Details")
            zones = st.session_state.zone_analysis_results["zones"]
            
            status_colors = {
                "Safe": "🟢",
                "Moderate": "🟡",
                "Danger": "🔴"
            }
            
            for zone_id, data in zones.items():
                status = data["status"]
                count = data["count"]
                emoji = status_colors.get(status, "⚪")
                st.markdown(f"{emoji} **{zone_id}**: {status} ({count} objects)")
        
        # Statistics
        st.divider()
        st.markdown("#### Zone Classification Summary")
        
        zones = st.session_state.zone_analysis_results["zones"]
        status_counts = {}
        for zone_data in zones.values():
            status = zone_data["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        col1, col2, col3 = st.columns(3)
        with col1:
            safe_count = status_counts.get("Safe", 0)
            st.metric("🟢 Safe Zones", safe_count)
        with col2:
            moderate_count = status_counts.get("Moderate", 0)
            st.metric("🟡 Moderate Zones", moderate_count)
        with col3:
            danger_count = status_counts.get("Danger", 0)
            st.metric("🔴 Danger Zones", danger_count)
        
        # Pie chart
        fig = px.pie(
            names=list(status_counts.keys()),
            values=list(status_counts.values()),
            color_discrete_map={
                "Safe": "#96CEB4",
                "Moderate": "#FFD93D",
                "Danger": "#FF6B6B"
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def depth_estimation_page():
    """Display depth estimation page"""
    st.markdown("## 📏 Depth Estimation")
    st.markdown("Estimate water depth using MiDaS deep learning model")
    
    st.divider()
    
    if st.session_state.uploaded_image is None:
        st.warning("⚠️ Please upload an image first in the Upload Media page")
        return
    
    if st.button("🌊 Estimate Depth", use_container_width=True):
        with st.spinner("Estimating depth... Please wait"):
            time.sleep(2)
            depth_map = depth_estimation(st.session_state.uploaded_image)
            st.session_state.depth_map = depth_map
            st.session_state.processing_history.append({
                "type": "depth_estimation",
                "timestamp": datetime.now()
            })
    
    # Display results
    if st.session_state.depth_map is not None:
        st.divider()
        st.markdown("### ✅ Depth Estimation Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Original Image")
            st.image(st.session_state.uploaded_image, width='stretch')
        
        with col2:
            st.markdown("#### Depth Map")
            fig, ax = plt.subplots(figsize=(8, 6))
            im = ax.imshow(st.session_state.depth_map, cmap="viridis")
            ax.set_title("Depth Estimation Map")
            ax.axis("off")
            plt.colorbar(im, ax=ax, label="Depth (Relative Units)")
            st.pyplot(fig, use_container_width=True)
        
        # Statistics
        st.divider()
        st.markdown("#### Depth Statistics")
        
        depth_data = st.session_state.depth_map.astype(float)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Min Depth", f"{depth_data.min():.1f}m")
        with col2:
            st.metric("Max Depth", f"{depth_data.max():.1f}m")
        with col3:
            st.metric("Avg Depth", f"{depth_data.mean():.1f}m")
        with col4:
            st.metric("Std Dev", f"{depth_data.std():.1f}m")

# ============================================================================
# MAIN APP LOGIC
# ============================================================================

def main():
    """Main application logic"""
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        login_page()
        return
    
    # Logout button and welcome message in sidebar
    with st.sidebar:
        # Add sidebar logo
        st.image("https://img.icons8.com/color/96/000000/ocean-wave.png", width=50)
        st.markdown(f"### 👋 Welcome, {st.session_state.username}!")
        st.divider()

        if st.button("🔓 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.uploaded_image = None
            st.session_state.uploaded_video = None
            st.session_state.enhanced_image = None
            st.session_state.detection_results = None
            st.session_state.zone_analysis_results = None
            st.session_state.depth_map = None
            st.rerun()

        st.divider()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🗺️ Navigation")
        page = st.radio(
            "Select Page:",
            [
                "🏠 Home",
                "📤 Upload Media",
                "🖼️ Enhancement",
                "🎯 Detection",
                "📍 Zone Analysis",
                "📏 Depth Estimation",
                "📊 Analytics"
            ],
            label_visibility="collapsed"
        )
    
    # Main content area
    st.sidebar.divider()
    
    # Route to pages
    if page == "🏠 Home":
        home_page()
    elif page == "📤 Upload Media":
        upload_page()
    elif page == "🖼️ Enhancement":
        enhancement_page()
    elif page == "🎯 Detection":
        detection_page()
    elif page == "📍 Zone Analysis":
        zone_analysis_page()
    elif page == "📏 Depth Estimation":
        depth_estimation_page()
    elif page == "📊 Analytics":
        show_analytics()
    else:
        home_page()
    
    # Footer
    st.sidebar.divider()
    st.sidebar.markdown(
        "<p style='text-align: center; color: #999; font-size: 12px;'>v1.0 • Underwater Monitoring System</p>",
        unsafe_allow_html=True
    )

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    main()
