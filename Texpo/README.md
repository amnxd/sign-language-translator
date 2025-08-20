# Hand Gesture Recognition FastAPI 🤚🚀

A high-performance FastAPI-based web service for real-time hand gesture recognition using MediaPipe and TensorFlow Lite. This API provides comprehensive endpoints to analyze images and detect hand gestures, including static hand signs and finger movement patterns.

## ✨ Features

- 🤚 **Hand Gesture Detection**: Recognizes static hand gestures (peace sign, rock&roll, awesome, OK, stop)
- 👆 **Finger Movement Tracking**: Detects finger movement patterns (clockwise, counter-clockwise, stop, move)
- 🖼️ **Multi-Format Support**: File upload, base64 encoding, and batch processing
- 📊 **Visual Feedback**: Optional visualization with hand landmarks and bounding boxes
- ⚙️ **Highly Configurable**: Adjustable confidence thresholds and detection parameters
- 🚀 **Performance Optimized**: Efficient processing with performance monitoring
- 📡 **RESTful API**: Clean REST endpoints with comprehensive documentation
- 🌐 **Interactive Demo**: Built-in web interface for testing
- 📈 **Analytics**: Detection statistics and performance metrics
- 🔄 **Batch Processing**: Analyze multiple images simultaneously

## Available Gestures

### Hand Gestures
- **Peace Sign** (✌️)
- **Rock & Roll** (🤘)
- **Awesome** (👍)
- **OK** (👌)
- **Stop** (✋)

### Finger Movements
- **Stop** - No movement
- **Clockwise** - Circular clockwise motion
- **Counter Clockwise** - Circular counter-clockwise motion
- **Move** - General movement

## Installation

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd D:\Code\sign-language-translator\Texpo
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify model files exist:**
   - `hand-gesture-recognition-mediapipe/model/keypoint_classifier/keypoint_classifier.tflite`
   - `hand-gesture-recognition-mediapipe/model/point_history_classifier/point_history_classifier.tflite`

## Quick Start

### Start the Server

```bash
# Method 1: Direct execution
python main.py

# Method 2: Using uvicorn with auto-reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Method 3: Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Test the API

```bash
# Run the test script
python test_api.py
```

## API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and available gestures |
| `/health` | GET | Health check and model status |
| `/gestures` | GET | List of available gestures and movements |
| `/model-info` | GET | Detailed model information |

### Image Processing

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analyze-image` | POST | Upload and analyze image file |
| `/process-base64` | POST | Process base64 encoded image |
| `/batch-analyze` | POST | Analyze multiple images at once (max 10) |
| `/analyze-with-stats` | POST | Analyze image with detailed statistics |

### Configuration

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/config` | GET | Get current analysis configuration |
| `/config` | POST | Update analysis configuration |

### Advanced Features

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/demo-ui` | GET | Interactive HTML demo interface |
| `/performance-test` | GET | Test API performance and model status |

## Usage Examples

### 1. Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": {
    "gesture_recognizer": true,
    "keypoint_classifier": true,
    "point_history_classifier": true
  }
}
```

### 2. Get Available Gestures

```bash
curl -X GET "http://localhost:8000/gestures"
```

**Response:**
```json
{
  "hand_gestures": {
    "0": "peace sign",
    "1": "rock&roll",
    "2": "awesome",
    "3": "OK",
    "4": "Stop"
  },
  "finger_movements": {
    "0": "Stop",
    "1": "Clockwise",
    "2": "Counter Clockwise",
    "3": "Move"
  }
}
```

### 3. Analyze Image File

```bash
curl -X POST "http://localhost:8000/analyze-image" \
  -F "file=@hand_image.jpg" \
  -F "include_visualization=true"
```

### 4. Process Base64 Image

```bash
curl -X POST "http://localhost:8000/process-base64" \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD...",
    "include_landmarks": true,
    "include_visualization": true
  }'
```

**Response:**
```json
{
  "detected_hands": [
    {
      "gesture_id": 0,
      "gesture_label": "peace sign",
      "confidence": null,
      "hand_landmarks": [[240, 180], [245, 185], ...],
      "bounding_rect": [200, 150, 350, 300]
    }
  ],
  "processed_image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD...",
  "fps": null
}
```

### 5. Update Configuration

```bash
curl -X POST "http://localhost:8000/config" \
  -H "Content-Type: application/json" \
  -d '{
    "min_detection_confidence": 0.8,
    "min_tracking_confidence": 0.6,
    "max_num_hands": 2,
    "use_static_image_mode": false
  }'
```

### 6. Batch Process Multiple Images

```bash
curl -X POST "http://localhost:8000/batch-analyze" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "files=@image3.jpg" \
  -F "include_visualization=false" \
  -F "include_landmarks=true"
```

**Response:**
```json
{
  "total_processed": 3,
  "results": [
    {
      "filename": "image1.jpg",
      "index": 0,
      "error": null,
      "detected_hands": [...]
    },
    {
      "filename": "image2.jpg",
      "index": 1,
      "error": null,
      "detected_hands": [...]
    }
  ]
}
```

### 7. Analyze with Statistics

```bash
curl -X POST "http://localhost:8000/analyze-with-stats" \
  -F "file=@hand_image.jpg" \
  -F "include_visualization=true"
```

**Response:**
```json
{
  "detected_hands": [...],
  "processed_image_base64": "data:image/jpeg;base64,...",
  "statistics": {
    "total_detections": 2,
    "gesture_counts": {
      "peace sign": 1,
      "OK": 1
    },
    "most_common_gesture": "peace sign",
    "detection_rate": 1.0
  },
  "processing_time_seconds": 0.234,
  "image_dimensions": {
    "width": 640,
    "height": 480
  }
}
```

### 8. Interactive Demo Interface

Visit `http://localhost:8000/demo-ui` in your browser for a web-based interface to test the API.

### 9. Performance Test

```bash
curl -X GET "http://localhost:8000/performance-test"
```

**Response:**
```json
{
  "performance_test": {
    "total_time_seconds": 0.123,
    "models_loaded": {
      "gesture_recognizer": true,
      "keypoint_classifier": true,
      "point_history_classifier": true
    },
    "test_detection_successful": true,
    "available_gestures_count": 5,
    "available_movements_count": 4
  }
}
```

## Python Client Example

```python
import requests
import base64

# Initialize API client
api_base = "http://localhost:8000"

# Load and encode image
with open("hand_image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# Process image
payload = {
    "image_base64": f"data:image/jpeg;base64,{image_data}",
    "include_landmarks": True,
    "include_visualization": True
}

response = requests.post(f"{api_base}/process-base64", json=payload)
result = response.json()

# Print results
for hand in result["detected_hands"]:
    print(f"Detected: {hand['gesture_label']} (ID: {hand['gesture_id']})")
    print(f"Bounding box: {hand['bounding_rect']}")
```

## Response Models

### GestureResult
```json
{
  "gesture_id": 0,
  "gesture_label": "peace sign",
  "confidence": null,
  "hand_landmarks": [[x1, y1], [x2, y2], ...],
  "bounding_rect": [x_min, y_min, x_max, y_max]
}
```

### ProcessImageResponse
```json
{
  "detected_hands": [GestureResult, ...],
  "processed_image_base64": "data:image/jpeg;base64,...",
  "fps": null
}
```

## Configuration Options

- `min_detection_confidence`: Minimum confidence for hand detection (0.0-1.0)
- `min_tracking_confidence`: Minimum confidence for hand tracking (0.0-1.0)
- `max_num_hands`: Maximum number of hands to detect (1-2)
- `use_static_image_mode`: Whether to use static image mode

## Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Error Handling

The API returns standard HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid image format, etc.)
- `500`: Internal Server Error (model loading issues, processing errors)

## Performance Tips

1. **Image Size**: Resize large images before processing for better performance
2. **Confidence Thresholds**: Adjust detection confidence based on your use case
3. **Static Mode**: Enable static image mode for better accuracy on static images
4. **Landmarks**: Disable landmark output if not needed to reduce response size

## Troubleshooting

### Models Not Loading
- Ensure model files exist in the correct paths
- Check file permissions
- Verify TensorFlow Lite installation

### Poor Detection Accuracy
- Ensure good lighting conditions
- Position hands clearly in frame
- Adjust confidence thresholds
- Use higher resolution images

### API Connection Issues
- Verify the server is running on the correct port
- Check firewall settings
- Ensure all dependencies are installed

## Dependencies

- FastAPI: Web framework
- MediaPipe: Hand detection and landmark estimation
- TensorFlow Lite: Gesture classification
- OpenCV: Image processing
- Uvicorn: ASGI server

See `requirements.txt` for complete dependency list.

## License

This project uses the hand-gesture-recognition-mediapipe models and utilities. Please refer to the original project's license terms.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Run the test script to verify setup
4. Check server logs for error details
