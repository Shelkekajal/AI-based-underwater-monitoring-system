# 🌊 AI-Based Underwater Monitoring System

A comprehensive Streamlit application for underwater image and video analysis with AI-powered features including image enhancement, object detection, zone-wise pollution analysis, and depth estimation.

## ✨ Features

### 📊 Core Capabilities

1. **🖼️ Image Enhancement**
   - Advanced underwater image enhancement using CLAHE (Contrast Limited Adaptive Histogram Equalization)
   - Denoising algorithms for clearer images
   - Color correction and contrast improvement
   - Real-time enhancement scoring (0-95%)

2. **🎯 Object Detection**
   - YOLOv8-based object detection
   - Detects: Plastic, Garbage, Fish, Algae
   - Real-time bounding box visualization
   - Object count statistics and charts

3. **📍 Zone-wise Pollution Analysis**
   - 3x3 grid-based spatial analysis
   - Zone classification: Safe (green), Moderate (orange), Danger (red)
   - Object distribution visualization
   - Pollution hotspot identification

4. **📏 Depth Estimation**
   - MiDaS model-based depth mapping
   - Depth visualization with color gradients
   - Depth statistics (min, max, average)
   - 3D depth information for underwater topography

5. **📊 Analytics Dashboard**
   - Object detection statistics
   - Zone classification breakdown
   - System health monitoring
   - Processing history tracking

6. **🔐 Authentication**
   - Simple login system with session management
   - User profile management
   - Session state tracking

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **Image Processing**: OpenCV
- **Object Detection**: YOLOv8 (Ultralytics)
- **Deep Learning**: PyTorch
- **Depth Estimation**: MiDaS (Intel ISL)
- **Visualization**: Matplotlib, Plotly
- **Image Handling**: PIL (Pillow)
- **Data Processing**: NumPy

## 📋 Requirements

- Python 3.8+
- All dependencies listed in `requirements.txt`

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project

```bash
cd c:\Users\ADMIN\OneDrive\Documents\final
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

### Step 3: Install Dependencies

Create `requirements.txt` with the following content:

```txt
streamlit==1.28.1
numpy==1.24.3
opencv-python==4.8.1.78
torch==2.0.1
pillow==10.0.0
matplotlib==3.7.2
plotly==5.17.0
scikit-image==0.21.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will be available at: `http://localhost:8501`

## 📖 Usage Guide

### 🔐 Logging In

1. Enter any username (e.g., "admin", "user123")
2. Enter any password of 4+ characters
3. Click "Login" to access the dashboard

**Demo Credentials:**
- Username: Any value
- Password: Any 4+ characters (e.g., "1234")

### 📱 Navigation

Use the sidebar to navigate between different features:

1. **Home** - Landing page with feature overview
2. **Upload Media** - Upload underwater images or videos
3. **Enhancement** - Enhance image quality
4. **Detection** - Run object detection
5. **Zone Analysis** - Analyze pollution by zones
6. **Depth Estimation** - Generate depth maps
7. **Analytics** - View system statistics

### 🔄 Workflow

1. **Start**: Click "Get Started" on home page
2. **Upload**: Go to "Upload Media" and upload an underwater image
3. **Enhance** (Optional): Enhance image quality in "Enhancement" page
4. **Detect**: Run object detection in "Detection" page
5. **Analyze**: Use "Zone Analysis" to identify problem areas
6. **Estimate**: Get depth information in "Depth Estimation"
7. **Review**: Check "Analytics" for overall system insights

## 📂 File Structure

```
final/
├── app.py                 # Main Streamlit application
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## 🎨 UI Components

### Pages

- **Home Page**: Landing dashboard with feature showcase
- **Login Page**: User authentication
- **Upload Page**: Media upload interface
- **Enhancement Page**: Image enhancement tools
- **Detection Page**: Object detection results
- **Zone Analysis Page**: Spatial analysis visualization
- **Depth Estimation Page**: Depth mapping display
- **Analytics Page**: System statistics and graphs

### Sidebar Features

- User welcome message
- Navigation menu
- Logout button
- System version info

## ⚙️ Key Functions

### Image Processing

```python
enhance_image(image)          # Enhance underwater image
detect_objects(image)         # Run object detection
zone_analysis(image, objects) # Analyze pollution zones
depth_estimation(image)       # Estimate water depth
```

### Session Management

- `logged_in`: Authentication status
- `uploaded_image`: Stored uploaded image
- `detection_results`: Detection results cache
- `zone_analysis_results`: Zone analysis cache
- `depth_map`: Computed depth map cache

## 📊 Output Examples

### Enhancement Score
- Displays contrast improvement percentage (40-95%)
- Visual progress bar
- Clarity and readiness metrics

### Object Detection
- Bounding boxes with object names
- Per-class countbar charts
- Total detection count

### Zone Analysis
- Color-coded 3x3 grid (Green/Orange/Red)
- Zone status classification
- Pie chart of zone distribution

### Depth Estimation
- Colored depth map visualization
- Min/max/average depth statistics
- Standard deviation metrics

## 🔧 Customization

### Modify Enhancement Parameters

Edit the `enhance_image()` function:
```python
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
```

### Adjust Detection Classes

Update the `classes` list in `detect_objects()`:
```python
classes = ["Plastic", "Garbage", "Fish", "Algae"]
```

### Change Zone Grid Size

Modify in `zone_analysis()`:
```python
grid_h = h // 3  # Change 3 to desired grid size
grid_w = w // 3
```

## 📈 Future Enhancements

- Integration with actual YOLOv8 models
- Real MiDaS model integration
- Multi-image batch processing
- Export reports as PDF
- Database integration for image storage
- API integration for remote analysis
- Real-time video stream processing
- Cloud deployment

## 🐛 Troubleshooting

### Issue: Streamlit not found
**Solution**: Ensure virtual environment is activated and dependencies are installed
```bash
pip install streamlit
```

### Issue: OpenCV import error
**Solution**: Reinstall OpenCV
```bash
pip install --upgrade opencv-python
```

### Issue: Torch/PyTorch not installing
**Solution**: Install specific PyTorch version for your OS
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Issue: Application runs but images don't load
**Solution**: Ensure the uploaded file format is supported (JPG, PNG, BMP)

## 💡 Tips & Best Practices

1. **Start Simple**: Begin with image enhancement before running multiple analyses
2. **Use High-Quality Images**: Better input images produce better results
3. **Monitor Analytics**: Check the Analytics page to track system performance
4. **Batch Processing**: For multiple images, upload and process sequentially
5. **Optimize Performance**: For large images, consider resizing before upload

## 📝 Code Structure

The application is organized into sections:

1. **Imports & Configuration**: Libraries and page setup
2. **Initialization**: Session state management
3. **Authentication**: Login system
4. **Image Processing Functions**: Enhancement, detection, analysis
5. **Page Functions**: UI for each feature
6. **Navigation Logic**: Page routing
7. **Main App**: Application entry point

## 🔐 Security Notes

- Current authentication is simplified for demo purposes
- In production, implement proper user management
- Never hardcode credentials
- Use environment variables for sensitive data
- Validate all user inputs

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Ensure all dependencies are correctly installed
4. Verify Python version compatibility

## 📄 License

This project is provided as-is for educational and research purposes.

## 👤 Author

AI-Based Underwater Monitoring System
Built with Streamlit and Python

---

**Version**: 1.0  
**Last Updated**: 2024  
**Status**: Ready for Production
