from http.server import BaseHTTPRequestHandler
import requests
import base64
import json
import cgi

ROBOFLOW_API_KEY = "FVqfVxwUgjQmJHhmr2sR"
MODEL_ENDPOINT   = "retail-store-detection-cv-p6zlc/4"
ROBOFLOW_URL     = f"https://detect.roboflow.com/{MODEL_ENDPOINT}"


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        try:
            content_type = self.headers.get("Content-Type", "")
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            # Parse multipart form data
            if "multipart/form-data" in content_type:
                boundary = content_type.split("boundary=")[-1].encode()
                image_bytes = self._extract_file_from_multipart(body, boundary)
            else:
                self._respond(400, {"error": "Expected multipart/form-data"})
                return

            if not image_bytes:
                self._respond(400, {"error": "No image file found in request"})
                return

            # Call Roboflow
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            resp = requests.post(
                ROBOFLOW_URL,
                params={
                    "api_key":    ROBOFLOW_API_KEY,
                    "confidence": 0.4,
                    "overlap":    0.3,
                },
                data=image_base64,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=25,
            )
            resp.raise_for_status()
            data = resp.json()

            predictions   = data.get("predictions", [])
            details       = []
            product_count = 0
            missing_count = 0

            for p in predictions:
                cls = p.get("class", "unknown").lower()
                is_missing = any(w in cls for w in ["missing", "empty", "gap", "hole", "vacant"])

                if is_missing:
                    missing_count += 1
                    category = "missing"
                else:
                    product_count += 1
                    category = "product"

                details.append({
                    "class":      category,
                    "x":          p.get("x", 0),
                    "y":          p.get("y", 0),
                    "width":      p.get("width", 0),
                    "height":     p.get("height", 0),
                    "confidence": p.get("confidence", 0),
                })

            result = {
                "status": "success",
                "summary": {
                    "total_products_detected": product_count,
                    "total_missing_detected":  missing_count,
                },
                "details": details,
                "business_mapping": {
                    "restock_required": missing_count > 0,
                    "severity": (
                        "high"   if missing_count > 5 else
                        "medium" if missing_count > 2 else
                        "low"    if missing_count > 0 else
                        "none"
                    ),
                },
            }
            self._respond(200, result)

        except requests.RequestException as e:
            self._respond(502, {"error": f"Roboflow API error: {str(e)}"})
        except Exception as e:
            self._respond(500, {"error": str(e)})

    # ── helpers ──────────────────────────────────────────────────────────────

    def _extract_file_from_multipart(self, body: bytes, boundary: bytes) -> bytes:
        """Very small multipart parser — extracts the first file part."""
        delimiter = b"--" + boundary
        parts = body.split(delimiter)
        for part in parts:
            if b"Content-Disposition" in part and b'filename="' in part:
                # Split headers from body at the double CRLF
                if b"\r\n\r\n" in part:
                    _, file_data = part.split(b"\r\n\r\n", 1)
                    return file_data.rstrip(b"\r\n--")
        return b""

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")

    def _respond(self, status: int, payload: dict):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type",   "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)