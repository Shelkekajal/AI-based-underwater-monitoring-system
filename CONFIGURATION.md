# ⚙️ Configuration Guide

This guide explains how to customize the Underwater Monitoring System for different use cases.

## 🎨 Customization Options

### 1. Enhancement Parameters

Edit the `enhance_image()` function in `app.py` to adjust image enhancement:

```python
# CLAHE (Contrast Limited Adaptive Histogram Equalization)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
```

**Parameters:**
- `clipLimit`: Higher values increase contrast (0.1 - 5.0)
  - Lower (0.5-1.0): Softer enhancement
  - Higher (3.0-5.0): More aggressive enhancement
- `tileGridSize`: Grid size for local processing (4x4 to 16x16)
  - Smaller grids: More detailed enhancement
  - Larger grids: Smoother overall enhancement

**Denoising parameters:**
```python
enhanced = cv2.fastNlMeansDenoisingColored(img_array, None, h=10, hForColorComponents=10, templateWindowSize=7, searchWindowSize=21)
```

- `h`: Filter strength (5-20, higher = more denoising)
- `templateWindowSize`: Template patch size (must be odd)
- `searchWindowSize`: Search region size

---

### 2. Object Detection Classes

Register custom objects in `detect_objects()` function:

```python
classes = ["Plastic", "Garbage", "Fish", "Algae", "Coral", "Debris"]
```

**Add new class colors:**
```python
color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)][class_idx]
```

**Color format**: (B, G, R) in BGR, e.g., (255, 0, 0) = Blue

---

### 3. Zone Grid Configuration

Modify grid size in `zone_analysis()` function:

**Current (3x3 grid):**
```python
grid_h = h // 3
grid_w = w // 3
```

**For 4x4 grid:**
```python
grid_h = h // 4
grid_w = w // 4
```

**For 5x5 grid:**
```python
grid_h = h // 5
grid_w = w // 5
```

**Update zone iteration:**
```python
for i in range(3):  # Change 3 to grid dimension
    for j in range(3):  # Change 3 to grid dimension
```

**Adjust zone thresholds:**
```python
if zone_count == 0:
    status = "Safe"
elif zone_count <= total_objects // 9:  # Adjust threshold
    status = "Moderate"
else:
    status = "Danger"
```

---

### 4. Zone Status Colors

Customize safety classification colors in `zone_analysis_page()`:

```python
color_map = {
    "Safe": (0, 255, 0),      # Green
    "Moderate": (0, 165, 255), # Orange
    "Danger": (0, 0, 255)      # Red
}
```

**Status thresholds:**
- Modify zone classification logic to match your pollution standards
- Adjust object count limits based on acceptable levels

---

### 5. Depth Estimation Visualization

Modify depth map parameters in `depth_estimation()`:

```python
# Simulate depth map parameters
depth_map = 100 * (0.5 + 0.3 * np.sin(5 * X) + 0.2 * np.cos(5 * Y) + 0.3 * np.sqrt(X**2 + Y**2))
```

**Depth scale:**
```python
depth_map = ((depth_map - depth_map.min()) / (depth_map.max() - depth_map.min()) * 255).astype(np.uint8)
```

Change `255` to different max depth value for different scale.

**Visualization colormap** in `depth_estimation_page()`:
```python
fig, ax = plt.subplots()
im = ax.imshow(st.session_state.depth_map, cmap="viridis")  # Change colormap
```

Available colormaps: `viridis`, `plasma`, `inferno`, `magma`, `cividis`, `terrain`, `ocean`, `cool`, `hot`

---

### 6. Analytics Charts

Customize chart appearance in `show_analytics()`:

**Bar chart colors:**
```python
color_discrete_map={
    "Plastic": "#FF6B6B",
    "Garbage": "#4ECDC4",
    "Fish": "#45B7D1",
    "Algae": "#96CEB4"
}
```

**Pie chart colors:**
```python
color_discrete_map={
    "Safe": "#96CEB4",      # Green
    "Moderate": "#FFD93D",  # Yellow
    "Danger": "#FF6B6B"     # Red
}
```

**Chart layout:**
```python
fig.update_layout(height=400, showlegend=False, template="plotly_white")
```

---

### 7. Sidebar Styling

Modify sidebar appearance in the main section:

```python
# Edit sidebar markdown sections
st.markdown("### 🗺️ Navigation")
st.markdown("### 👋 Welcome, {username}!")
```

---

### 8. Page Colors & Themes

Update color scheme throughout:

```python
# Primary color for headings
"color: #1f77b4;"  # Blue

# Adjust to other colors:
# #FF6B6B - Red
# #4ECDC4 - Teal
# #45B7D1 - Light Blue
# #96CEB4 - Green
# #FFB347 - Orange
```

---

### 9. Session State Variables

Add new tracked variables in `init_session_state()`:

```python
if 'my_custom_var' not in st.session_state:
    st.session_state.my_custom_var = None
```

---

### 10. Processing History

Customize what's tracked in processing history:

```python
st.session_state.processing_history.append({
    "type": "enhancement",
    "timestamp": datetime.now(),
    "score": score,
    "custom_metric": value  # Add custom fields
})
```

---

## 🔧 Advanced Configuration

### Enable Real YOLOv8 Detection

Replace the simulated detection with actual YOLOv8:

```python
from ultralytics import YOLO

def detect_objects(image):
    # Load pre-trained YOLOv8 model
    model = YOLO('yolov8n.pt')
    
    # Run inference
    results = model(image)
    
    # Process results
    # ...
    return annotated_image, detected_objects
```

**Install ultralytics:**
```bash
pip install ultralytics
```

---

### Integration with MiDaS Depth Model

Replace simulated depth with real MiDaS:

```python
import torch

def depth_estimation(image):
    # Load MiDaS model
    midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
    midas.eval()
    
    # Prepare image
    transform = torch.hub.load("intel-isl/MiDaS", "transforms").composition.transforms
    
    # Run inference
    # ...
    return depth_map
```

---

### Database Integration

Add persistent storage:

```python
import sqlite3

def save_analysis(username, image_name, results):
    conn = sqlite3.connect("underwater_monitoring.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO analyses VALUES (?, ?, ?)""", 
                   (username, image_name, str(results)))
    conn.commit()
    conn.close()
```

---

## 🎯 Performance Optimization

### 1. Image Resizing
Add before processing:
```python
max_size = 1024
image = image.resize((max_size, max_size), Image.Resampling.LANCZOS)
```

### 2. Caching
```python
@st.cache_resource
def load_model():
    # Load model once
    return model
```

### 3. Batch Processing
```python
for image in image_list:
    process_image(image)
    st.progress(count / total)
```

---

## 📊 Custom Analytics

Add new metrics to analytics page:

```python
st.markdown("#### Custom Metric")
st.metric("Metric Name", value)

# Custom chart
fig = px.scatter(x=data_x, y=data_y)
st.plotly_chart(fig)
```

---

## 🔐 Security Settings

### Username/Password Validation
```python
if username and len(username) >= 3:
    if len(password) >= 8:  # Require 8 chars
        # Authenticate
```

### Input Sanitization
```python
username = username.strip()
password = hashlib.sha256(password.encode()).hexdigest()
```

---

## 🚀 Deployment Configuration

### Streamlit Config File
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"

[server]
maxUploadSize = 50
enableXsrfProtection = true
```

### Environment Variables
Create `.env`:
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

---

## 📝 Logging & Debugging

Add logging:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Processing image...")
```

---

## 📚 Resource Limits

Set limits in `init_session_state()`:
```python
st.session_state.max_images = 100
st.session_state.max_processing_time = 60  # seconds
```

---

This guide covers most customization scenarios. For more advanced modifications, review the code comments and Streamlit documentation.
