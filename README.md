# 🏪 Retail Inventory Scanner - AI-Powered CCTV Product Detection

An advanced computer vision system for real-time retail shelf monitoring using YOLOv8 object detection. This application automatically identifies products and detects empty shelf spaces, providing instant alerts for inventory management.

## 🎯 Features

- **Real-Time Detection**: Continuously monitors shelf inventory with high accuracy
- **AI-Powered Analysis**: Uses YOLOv8 model hosted on Roboflow for object detection
- **Visual Annotations**: Provides clear bounding boxes around detected products and gaps
- **Instant Alerts**: Automatically generates alerts when missing items are detected
- **Multi-Camera Support**: Monitor multiple aisles simultaneously (9 cameras)
- **Interactive Dashboard**: View analytics and insights across all monitored locations
- **Live Testing Mode**: Upload images directly from mobile devices via QR code
- **Business Intelligence**: Get actionable insights about restocking priorities

## 🚀 Demo

### Main Camera Grid
Monitor multiple aisles in real-time with live detection status.

### AI Detection Results
Visual annotations with bounding boxes for products (green) and missing items (red).

### Analytics Dashboard
Comprehensive charts showing detection statistics across all aisles.

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance web framework
- **Python 3.8+**: Core programming language
- **Roboflow API**: Model hosting and inference
- **YOLOv8**: State-of-the-art object detection model

### Frontend
- **Vanilla JavaScript**: No frameworks, pure performance
- **HTML5/CSS3**: Modern, responsive design
- **Chart.js**: Interactive data visualizations
- **Canvas API**: Real-time image annotations

### AI/ML
- **YOLOv8**: Object detection architecture
- **Roboflow**: Model training and deployment platform
- **Custom Dataset**: Trained on retail shelf images
- **Classes**: `product` and `missing` detection

## 📋 Prerequisites

- Python 3.8 or higher
- Roboflow account with API access
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/retail-inventory-scanner.git
cd retail-inventory-scanner
```

### 2. Install Dependencies

```bash
pip install fastapi uvicorn python-multipart requests
```

Or use requirements.txt:

```bash
pip install -r requirements.txt
```

### 3. Configure Roboflow API

Update the `main.py` file with your Roboflow credentials:

```python
ROBOFLOW_API_KEY = "your_api_key_here"
MODEL_ENDPOINT = "your_model_endpoint/version"
```

### 4. Prepare Image Directory

Create an `images` folder in the root directory and add your sample images:

```
retail-inventory-scanner/
├── images/
│   ├── testupload1.jpg
│   ├── testupload2.jpg
│   ├── testupload3.jpg
│   ├── bogus.png
│   └── qrcode.png
├── index.html
├── main.py
└── README.md
```

## 🚀 Running the Application

### Start the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:8000
```

For mobile access via QR code:
```
http://your-ip-address:8000
```

## 📱 Usage

### Camera Grid View
1. View all 9 camera feeds on the main dashboard
2. Click "Inspect" on any camera to analyze detected items
3. Upload custom images to replace default feeds

### Inspect View
1. See original and AI-annotated images side-by-side
2. View detection statistics (products found, missing items)
3. Get instant restock alerts for empty spots
4. Review detailed analysis summaries

### Live Testing Mode
1. Click "Live" button in the header
2. Scan QR code with your mobile device
3. View static demonstration image
4. Perfect for showcasing the system

### Analytics Dashboard
1. Click "Dashboard" to view aggregated statistics
2. See overall product distribution (doughnut chart)
3. Compare per-aisle performance (bar chart)
4. Monitor total products and missing items

## 🎨 API Endpoints

### `GET /`
Serves the main HTML application.

**Response**: HTML page

### `POST /analyze-image`
Analyzes an uploaded image for product detection.

**Parameters**:
- `file`: Image file (JPG/PNG)
- `confidence`: Detection confidence threshold (default: 0.5)

**Response**:
```json
{
  "status": "OK",
  "summary": {
    "total_products_detected": 12,
    "total_missing_detected": 2
  },
  "annotated_image": "https://...",
  "details": [...],
  "business_mapping": {
    "restock_required": true,
    "severity": "low"
  }
}
```

### `GET /images/{filename}`
Serves static images from the images directory.

## 🏗️ Project Structure

```
retail-inventory-scanner/
├── main.py                 # FastAPI backend server
├── index.html             # Frontend application
├── images/                # Static image directory
│   ├── testupload1.jpg   # Sample camera feeds
│   ├── testupload2.jpg
│   ├── testupload3.jpg
│   ├── 2.jpg - 8.jpg     # Additional samples
│   ├── 77.jpg
│   ├── bogus.png         # Live demo image
│   └── qrcode.png        # Mobile access QR
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🤖 Model Details

### YOLOv8 Configuration
- **Architecture**: YOLOv8n (nano) for fast inference
- **Input Size**: 640x640 pixels
- **Classes**: 2 (product, missing)
- **Training Platform**: Roboflow
- **Inference**: Serverless deployment via Roboflow API

### Detection Classes
- **product**: Items present on shelf (Green box)
- **missing**: Empty spots or gaps (Red box)

### Performance
- **Confidence Threshold**: 50% (adjustable)
- **Overlap Threshold**: 30% (NMS)
- **Average Inference Time**: <100ms per image

## 🎨 Customization

### Adjust Detection Confidence

Modify the confidence parameter in `main.py`:

```python
confidence: float = 0.5  # Change to 0.3 for more detections
```

### Change Camera Count

Update the `state.cameras` array in `index.html` to add/remove cameras.

### Modify Visual Theme

Update CSS variables in the `<style>` section:

```css
--primary-color: #11A8B8;
--secondary-color: #8E5CFF;
--background: #0F172A;
```

## 🐛 Troubleshooting

### Backend Not Connecting
- Verify FastAPI server is running on port 8000
- Check CORS settings in `main.py`
- Ensure firewall allows connections

### Images Not Loading
- Verify `images/` directory exists
- Check file permissions
- Ensure image files are in JPG/PNG format

### Roboflow API Errors
- Verify API key is correct
- Check model endpoint format
- Ensure account has active subscription

### Detection Not Working
- Lower confidence threshold (try 0.3)
- Verify image quality and lighting
- Check if objects are within model's training domain

## 📊 Future Enhancements

- [ ] Real-time video stream processing
- [ ] Integration with inventory management systems
- [ ] Multi-store deployment support
- [ ] Historical analytics and reporting
- [ ] Email/SMS alert notifications
- [ ] Custom model training interface
- [ ] Mobile app for field staff
- [ ] Export reports to PDF/Excel


## 👤 Authors

**Your Name**
- GitHub: [@AsmaAfzi](https://github.com/AsmaAfzi)
- 


---

⭐ **Star this repository if you find it useful!**
