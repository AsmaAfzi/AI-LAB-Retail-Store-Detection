from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles  
import requests

# -----------------------------
# FastAPI App Setup
# -----------------------------
app = FastAPI(title="Retail Shelf Monitoring API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files (IMAGES)  <-- ADD THIS SECTION
# -----------------------------
app.mount("/images", StaticFiles(directory="images"), name="images")

# -----------------------------
# Serve index.html
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def serve_html():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# -----------------------------
# Roboflow Config
# -----------------------------
ROBOFLOW_API_KEY = "FVqfVxwUgjQmJHhmr2sR"
MODEL_ENDPOINT = "retail-store-detection-cv-p6zlc/4"
BASE_URL = f"https://serverless.roboflow.com/{MODEL_ENDPOINT}"

# -----------------------------
# Call Roboflow API
# -----------------------------
def call_roboflow(image_bytes: bytes, confidence: float = 0.5):
    url = (
        f"{BASE_URL}"
        f"?api_key={ROBOFLOW_API_KEY}"
        f"&confidence={confidence}"
        f"&overlap=0.3"
        f"&visualize=true"
    )

    response = requests.post(url, files={"file": image_bytes})

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Roboflow API error"
        )

    return response.json()

# -----------------------------
# Business Logic Mapping
# -----------------------------
def generate_business_report(predictions, annotated_image_url):
    total_products = sum(1 for p in predictions if p["class"] == "product")
    missing_items = sum(1 for p in predictions if p["class"] == "missing")

    return {
        "status": "OK" if missing_items == 0 else "Attention Needed",
        "summary": {
            "total_products_detected": total_products,
            "total_missing_detected": missing_items
        },
        "annotated_image": annotated_image_url,
        "details": predictions,
        "business_mapping": {
            "restock_required": missing_items > 0,
            "severity": "critical" if missing_items > 3 else "low"
        }
    }

# -----------------------------
# Analyze Image Route
# -----------------------------
@app.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    confidence: float = 0.5
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Only JPG or PNG images allowed")

    image_bytes = await file.read()

    result = call_roboflow(image_bytes, confidence)

    predictions = result.get("predictions", [])
    annotated_image_url = result.get("image", {}).get("url")

    return generate_business_report(predictions, annotated_image_url)
