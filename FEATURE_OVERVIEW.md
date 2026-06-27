# 🌊 Feature Overview & Architecture

## Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│           STREAMLIT UNDERWATER MONITORING SYSTEM             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │   Authentication    │
                    │   (Login/Logout)    │
                    └─────────────────────┘
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
            ┌────────┐  ┌────────┐  ┌────────┐
            │ Upload │  │ Process│  │ Analyze│
            │ Images │  │Images  │  │Results │
            └────────┘  └────────┘  └────────┘
                 │            │            │
    ┌────────────┴────────────┴────────────┴──────────┐
    │                                                   │
    ▼                ▼                 ▼                ▼
┌───────┐      ┌──────────┐      ┌──────────┐    ┌─────────┐
│Enhance│      │ Detect   │      │ Zone     │    │ Depth   │
│Image  │      │ Objects  │      │ Analysis │    │Estimate │
└───────┘      └──────────┘      └──────────┘    └─────────┘
    │               │                  │              │
    └───────────────┴──────────────────┴──────────────┘
                    │
                    ▼
            ┌──────────────────┐
            │  Analytics Dashboard
            │  & Visualization │
            └──────────────────┘
```

---

## 📱 Page Structure

### 1. **Home Page (Landing)**
```
┌─────────────────────────────────────────┐
│   🌊 Underwater Monitoring System       │
│   AI-Powered Ocean Health Analysis      │
├─────────────────────────────────────────┤
│                                         │
│  ✨ Key Features                        │
│  • 🖼️  Image Enhancement               │
│  • 🎯 Object Detection                 │
│  • 📍 Zone Analysis                    │
│  • 📏 Depth Estimation                 │
│                                         │
│  [Get Started Button]                   │
│                                         │
└─────────────────────────────────────────┘
```

### 2. **Login Page**
```
┌─────────────────────────────────┐
│   🌊 Underwater Monitoring      │
├─────────────────────────────────┤
│                                 │
│  Username: [________________]   │
│  Password: [________________]   │
│                                 │
│  [Login]  [Remember Me]         │
│                                 │
│  Demo: any user / 4+ chars pwd  │
│                                 │
└─────────────────────────────────┘
```

### 3. **Sidebar Navigation**
```
┌──────────────────────┐
│  👋 Welcome, User!   │
├──────────────────────┤
│ [🔓 Logout]          │
├──────────────────────┤
│  Navigation          │
│  ○ 🏠 Home          │
│  ○ 📤 Upload        │
│  ○ 🖼️  Enhancement  │
│  ○ 🎯 Detection     │
│  ○ 📍 Zone Analysis │
│  ○ 📏 Depth Est.    │
│  ○ 📊 Analytics     │
├──────────────────────┤
│  v1.0 • System Info  │
└──────────────────────┘
```

---

## 🖼️ Feature Pages

### **Upload Page**
```
┌─────────────────────────────────────────────────┐
│ 📤 Upload Media                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  Image              │  Video                    │
│  ┌──────────┐       │  ┌──────────┐            │
│  │ Upload   │       │  │ Upload   │            │
│  │  Image   │       │  │  Video   │            │
│  └──────────┘       │  └──────────┘            │
│  Format: JPG, PNG   │  Format: MP4, AVI        │
│  Max: 50MB          │  Max: 100MB              │
│                     │                          │
│  [Image Preview]    │  [Image Info]            │
│                     │  • Size: 1920x1080       │
│                     │  • Format: PNG           │
│                     │  • Mode: RGB             │
│                     │                          │
└─────────────────────────────────────────────────┘
```

### **Enhancement Page**
```
┌──────────────────────────────────────────────────┐
│ 🖼️  Image Enhancement                           │
├──────────────────────────────────────────────────┤
│                                                  │
│  [🚀 Enhance Image]                              │
│                                                  │
│  Original             │  Enhanced               │
│  ┌───────────┐        │  ┌───────────┐          │
│  │           │        │  │           │          │
│  │   Image   │        │  │  Improved │          │
│  │           │        │  │  Image    │          │
│  └───────────┘        │  └───────────┘          │
│                       │                        │
│  ─────────────────────────────────────────     │
│  📈 Enhancement Score: 88.5%                   │
│  █████████████████░░░░░░░░░░░░░░░░░░░░░░      │
│  • Contrast: ↑ 48.5%  | Clarity: High ✓        │
│  • Recommendation: Ready for Analysis           │
│  [⬇️  Download Enhanced Image]                  │
│                                                  │
└──────────────────────────────────────────────────┘
```

### **Detection Page**
```
┌────────────────────────────────────────────────────┐
│ 🎯 Object Detection (YOLOv8)                       │
├────────────────────────────────────────────────────┤
│                                                    │
│  [🔍 Detect Objects]                               │
│                                                    │
│  Image                    │  Object Counts        │
│  ┌─────────────┐          │  ┌────────────────┐   │
│  │ ┌─┐ ┌─┐     │          │  │ Plastic    5   │   │
│  │ │P│ │G│     │          │  │ Garbage    3   │   │
│  │ └─┘ └─┘     │          │  │ Fish       8   │   │
│  │ ┌─┐ ┌─┐     │          │  │ Algae      6   │   │
│  │ │F│ │A│     │          │  │ ────────────── │   │
│  │ └─┘ └─┘     │          │  │ Total      22  │   │
│  └─────────────┘          │  └────────────────┘   │
│                           │                       │
│  📊 Bar Chart             │                       │
│  Plastic  ██████          │                       │
│  Garbage  ████            │                       │
│  Fish     ██████████      │                       │
│  Algae    ████████        │                       │
│                                                    │
└────────────────────────────────────────────────────┘
```

### **Zone Analysis Page**
```
┌──────────────────────────────────────────┐
│ 📍 Zone-wise Pollution Analysis          │
├──────────────────────────────────────────┤
│                                          │
│  [📊 Analyze Zones]                      │
│                                          │
│  Zone Grid          │  Zone Details      │
│  ┌────┬────┬────┐   │  ┌──────────────┐  │
│  │🟢  │🟡  │🔴  │   │  │🟢 Zone 1-1   │  │
│  ├────┼────┼────┤   │  │   Safe (0)   │  │
│  │🟢  │🟢  │🟡  │   │  │ 🟡 Zone 1-2  │  │
│  ├────┼────┼────┤   │  │ Moderate (2) │  │
│  │🟡  │🔴  │🔴  │   │  │ 🔴 Zone 1-3  │  │
│  └────┴────┴────┘   │  │  Danger (5)  │  │
│                      │  └──────────────┘  │
│  Zone Stats:         │                    │
│  🟢 Safe: 4          │                    │
│  🟡 Moderate: 3      │                    │
│  🔴 Danger: 2        │                    │
│                      │                    │
│  [Pie Chart]         │                    │
│    Safe 44%          │                    │
│    Mod  34%          │                    │
│    Danger 22%        │                    │
│                                          │
└──────────────────────────────────────────┘
```

### **Depth Estimation Page**
```
┌────────────────────────────────────────────┐
│ 📏 Depth Estimation                        │
├────────────────────────────────────────────┤
│                                            │
│  [🌊 Estimate Depth]                       │
│                                            │
│  Original           │  Depth Map          │
│  ┌──────────────┐   │  ┌──────────────┐   │
│  │              │   │  │   Dark       │   │
│  │   Image      │   │  │  ▄▀▀▀▀▀▀▀▀▄ │   │
│  │              │   │  │ ▀▀▀▀▀▀▀▀▀▀▀  │   │
│  │              │   │  │  Bright  ▄▄▄ │   │
│  └──────────────┘   │  └──────────────┘   │
│                     │  (Viridis Cmap)     │
│                     │                     │
│  Depth Statistics:  │                     │
│  • Min Depth:   15.2m                    │
│  • Max Depth:   45.8m                    │
│  • Avg Depth:   28.5m                    │
│  • Std Dev:     10.2m                    │
│                                            │
└────────────────────────────────────────────┘
```

### **Analytics Page**
```
┌─────────────────────────────────────────────┐
│ 📊 System Analytics                         │
├─────────────────────────────────────────────┤
│                                             │
│  Metrics:                                   │
│  ┌────────┐  ┌────────┐  ┌────────┐ ┌─────┐
│  │Total   │  │ Avg    │  │ Images │ │ Sys │
│  │Detect  │  │Enhance │  │Process │ │Hlth │
│  │  22    │  │  88%   │  │   5    │ │ 95% │
│  └────────┘  └────────┘  └────────┘ └─────┘
│                                             │
│  Detection Counts        Zone Distribution  │
│  ┌──────────────┐       ┌──────────────┐   │
│  │█ Plastic  5  │       │ 🟢 Safe 44%  │   │
│  │█ Garbage  3  │       │ 🟡 Mod  34%  │   │
│  │█ Fish     8  │       │ 🔴 Danger22% │   │
│  │█ Algae    6  │       └──────────────┘   │
│  └──────────────┘                          │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

```
User Input (Image)
       │
       ▼
  Upload & Store
   (Session State)
       │
       ├─────────────┐
       │             │
       ▼             ▼
  Enhancement    Detection
       │             │
       ├─────┬───────┘
       │     │
       ▼     ▼
   Zone Analysis
       │
       ▼
  Depth Estimation
       │
       ▼
  Analytics & Results
       │
       ▼
   Display & Export
```

---

## 🎨 Color Scheme

```
Primary Colors:
• Header Blue:     #1f77b4
• Accent Teal:     #4ECDC4
• Success Green:   #96CEB4
• Warning Orange:  #FFD93D
• Danger Red:      #FF6B6B
• Light Blue:      #45B7D1
• Background:      #ffffff
• Secondary BG:    #f0f2f6
```

---

## 📊 Object Detection Classes

| Class | Color | Use Case |
|-------|-------|----------|
| Plastic | Red | Pollution indicator |
| Garbage | Teal | Debris detection |
| Fish | Light Blue | Marine life |
| Algae | Green | Plant growth |

---

## 🟢🟡🔴 Zone Classification

| Status | Color | Criteria | Action |
|--------|-------|----------|--------|
| Safe | Green | 0 objects | Continue monitoring |
| Moderate | Orange | 1-3 objects | Increase monitoring |
| Danger | Red | 4+ objects | Immediate cleanup |

---

## 📈 Enhancement Scoring

```
Score Range: 0-95%

0-30%:   Poor (Very low contrast)
30-60%:  Fair (Some improvement)
60-80%:  Good (Noticeable enhancement)
80-95%:  Excellent (High clarity)

Formula: 40 + (enhanced_contrast / original_contrast) × 50
```

---

## 🔐 Authentication Flow

```
┌─────────────┐
│ Login Page  │
└──────┬──────┘
       │
       ▼ (Enter Credentials)
   ┌────────────────────┐
   │ Validate Input     │
   │ (4+ char password) │
   └────┬───────────────┘
        │
        ├─ Invalid → Error Message
        │
        ├─ Valid → Set session_state
        │
        ▼
   ┌────────────────────┐
   │ Dashboard Access   │
   │ (Full Features)    │
   └────────────────────┘
```

---

## 🚀 Processing Pipeline

```
1. Image Upload
   ↓ (PIL Image)
   
2. Enhancement (Optional)
   ↓ (OpenCV CLAHE + Denoise)
   
3. Object Detection
   ↓ (YOLOv8 Simulation)
   
4. Zone Analysis
   ↓ (3x3 Grid Classification)
   
5. Depth Estimation
   ↓ (MiDaS Simulation)
   
6. Analytics Generation
   ↓ (Plotly Charts)
   
7. Results Display & Export
```

---

## 💾 Session State Variables

```
logged_in: bool                    # Auth status
username: str                      # User name
uploaded_image: PIL.Image          # Stored image
uploaded_video: File               # Stored video
enhanced_image: numpy.array        # Processed image
enhancement_score: float           # 0-95%
detection_results: dict            # {image, detections}
zone_analysis_results: dict        # {image, zones}
depth_map: numpy.array             # Depth visualization
processing_history: list           # {type, timestamp, data}
```

---

## 🔧 Key Functions & Complexity

| Function | Complexity | Time | Input | Output |
|----------|-----------|------|-------|--------|
| enhance_image | O(w×h) | 1s | Image | Image, Score |
| detect_objects | O(w×h) | 2s | Image | Image, Dict |
| zone_analysis | O(w×h) | 1s | Image, Dict | Image, Dict |
| depth_estimation | O(w×h) | 2s | Image | Array |

---

## 📦 Dependencies

```
Core:
├── streamlit         # Web framework
├── numpy             # Numerical computing
├── PIL/Pillow        # Image handling
├── opencv-python     # Image processing
├── matplotlib        # Visualization
└── plotly            # Interactive charts

Deep Learning:
├── torch             # Neural networks
└── scikit-image      # Image algorithms
```

---

## 🎯 User Workflows

### Workflow 1: Quick Analysis
```
Login → Upload → Detection → Zone Analysis → View Results
```

### Workflow 2: Detailed Analysis
```
Login → Upload → Enhancement → Detection → Zone → Depth → Analytics
```

### Workflow 3: Comparison
```
Upload → Enhance → View Side-by-Side → Download → Export
```

---

## 📞 Support & Documentation

- **README.md** - Detailed setup & user guide
- **QUICKSTART.md** - 5-minute startup guide
- **CONFIGURATION.md** - Customization options
- **Code Comments** - Inline explanations

---

**Ready to use the system?** Start with QUICKSTART.md! 🚀
