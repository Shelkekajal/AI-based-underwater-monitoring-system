# 🚀 Quick Start Guide

## Installation (5 minutes)

### 1. Open Command Prompt and Navigate to Project
```bash
cd c:\Users\ADMIN\OneDrive\Documents\final
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
streamlit run app.py
```

Your browser will automatically open at `http://localhost:8501`

---

## 🔐 First Login

1. Enter any username (e.g., `admin`, `demo`, `user123`)
2. Enter any password with 4+ characters (e.g., `1234`, `password`)
3. Click **Login**

---

## 📖 Step-by-Step Demo

### Phase 1: Upload an Image
1. Click **📤 Upload Media** from sidebar
2. Click "Choose an image..." button
3. Select any `.jpg`, `.png`, or `.bmp` file
4. View image information displayed

### Phase 2: Enhance Image
1. Click **🖼️ Enhancement** from sidebar
2. Click **🚀 Enhance Image** button
3. Wait for processing (1-2 seconds)
4. Compare Original vs Enhanced images
5. View Enhancement Score (85-95%)

### Phase 3: Detect Objects
1. Click **🎯 Detection** from sidebar
2. Click **🔍 Detect Objects** button
3. Wait for processing (2 seconds)
4. View annotated image with bounding boxes
5. Check object counts and bar chart

### Phase 4: Analyze Zones
1. Click **📍 Zone Analysis** from sidebar
2. Click **📊 Analyze Zones** button
3. View 3x3 grid with color coding:
   - 🟢 Green = Safe
   - 🟡 Orange = Moderate
   - 🔴 Red = Danger
4. Check zone statistics and pie chart

### Phase 5: Estimate Depth
1. Click **📏 Depth Estimation** from sidebar
2. Click **🌊 Estimate Depth** button
3. View depth map visualization
4. Check depth statistics (min, max, avg)

### Phase 6: View Analytics
1. Click **📊 Analytics** from sidebar
2. View system statistics and graphs
3. Check object detection trends
4. View zone classification distribution

---

## 🛠️ Troubleshooting Quick fixes

| Problem | Solution |
|---------|----------|
| Port 8501 already in use | `streamlit run app.py --server.port 8502` |
| ModuleNotFoundError | Make sure venv is activated: `venv\Scripts\activate` |
| Image won't load | Use .jpg or .png format, max 50MB |
| App is slow | Close other applications, use smaller images |

---

## 🎯 Key Features at a Glance

| Feature | What It Does | Time |
|---------|-------------|------|
| **Enhancement** | Improves image clarity and contrast | 1 sec |
| **Detection** | Finds plastic, garbage, fish, algae | 2 sec |
| **Zone Analysis** | Maps pollution across grid zones | 1 sec |
| **Depth Est.** | Generates depth visualization | 2 sec |
| **Analytics** | Shows system-wide statistics | Instant |

---

## 💻 System Requirements

- **OS**: Windows, Mac, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB for dependencies

---

## 📸 Supported File Formats

**Images**: `.jpg`, `.jpeg`, `.png`, `.bmp`  
**Videos**: `.mp4`, `.avi`, `.mov`, `.mkv`

---

## 🔄 Complete Workflow

```
Start
  ↓
Login → Home Page → Upload Image
  ↓
Enhancement → Detection → Zone Analysis → Depth Estimation
  ↓
Analytics → Review Results
  ↓
Logout
```

---

## 💡 Pro Tips

1. **Best Results**: Use clear underwater images with good lighting
2. **Faster Processing**: Start with smaller images (< 2MB)
3. **Compare Results**: Use the side-by-side views to see improvements
4. **Track Progress**: Check Analytics after each processing step
5. **Export Images**: Download enhanced images for external use

---

## 🆘 Need Help?

- Check **README.md** for detailed documentation
- Review code comments in **app.py**
- Ensure all dependencies are installed: `pip list`
- Verify Python version: `python --version`

---

**Ready to Start?** Run this command:
```bash
streamlit run app.py
```

Enjoy analyzing underwater environments! 🌊
