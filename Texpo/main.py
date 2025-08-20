#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hand Gesture Recognition FastAPI Application

This FastAPI application provides endpoints for real-time hand gesture recognition
using MediaPipe and TensorFlow Lite models. It integrates with the hand-gesture-recognition-mediapipe
module to detect and classify hand gestures from images.

Features:
- Hand gesture classification (peace sign, rock&roll, awesome, OK, stop)
- Finger movement pattern detection (clockwise, counter-clockwise, stop, move)
- Image processing via file upload or base64 encoding
- Real-time visualization with hand landmarks
- Configurable detection parameters
- RESTful API with comprehensive documentation
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import cv2 as cv
import numpy as np
import mediapipe as mp
import csv
import copy
import itertools
from collections import Counter, deque
import io
import base64
import asyncio
import json
import logging
import time
from typing import List, Dict, Optional, Union, Tuple
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the hand-gesture-recognition-mediapipe directory to Python path
import sys
module_path = os.path.join(os.path.dirname(__file__), 'hand-gesture-recognition-mediapipe')
if module_path not in sys.path:
    sys.path.insert(0, module_path)

try:
    # Import from the hand-gesture-recognition-mediapipe module
    from utils.cvfpscalc import CvFpsCalc
    from model.keypoint_classifier.keypoint_classifier import KeyPointClassifier
    from model.point_history_classifier.point_history_classifier import PointHistoryClassifier
    
    # Import processing functions directly from app.py
    from app import (
        calc_bounding_rect,
        calc_landmark_list,
        pre_process_landmark,
        pre_process_point_history,
        draw_landmarks,
        draw_bounding_rect,
        draw_info_text,
        draw_point_history,
        draw_info
    )
    
    logger.info("Successfully imported all modules from hand-gesture-recognition-mediapipe")
except ImportError as e:
    logger.error(f"Failed to import modules: {e}")
    logger.error("Make sure the hand-gesture-recognition-mediapipe directory is present and contains all required files")
    raise

app = FastAPI(
    title="Hand Gesture Recognition API",
    description="API for real-time hand gesture recognition using MediaPipe and TensorFlow Lite",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class GestureResult(BaseModel):
    gesture_id: int
    gesture_label: str
    confidence: Optional[float] = None
    hand_landmarks: Optional[List[List[int]]] = None
    bounding_rect: Optional[List[int]] = None

class ProcessImageRequest(BaseModel):
    image_base64: str
    include_landmarks: bool = True
    include_visualization: bool = True

class ProcessImageResponse(BaseModel):
    detected_hands: List[GestureResult]
    processed_image_base64: Optional[str] = None
    fps: Optional[float] = None

class AnalysisConfig(BaseModel):
    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.5
    max_num_hands: int = 2
    use_static_image_mode: bool = False

# Global variables for model initialization
gesture_recognizer = None
keypoint_classifier = None
point_history_classifier = None
keypoint_classifier_labels = []
point_history_classifier_labels = []
analysis_config = AnalysisConfig()

@app.on_event("startup")
async def startup_event():
    """Initialize models and load labels on startup"""
    global gesture_recognizer, keypoint_classifier, point_history_classifier
    global keypoint_classifier_labels, point_history_classifier_labels
    
    try:
        # Initialize MediaPipe Hands
        mp_hands = mp.solutions.hands
        gesture_recognizer = mp_hands.Hands(
            static_image_mode=analysis_config.use_static_image_mode,
            max_num_hands=analysis_config.max_num_hands,
            min_detection_confidence=analysis_config.min_detection_confidence,
            min_tracking_confidence=analysis_config.min_tracking_confidence,
        )
        
        # Initialize classifiers
        keypoint_classifier = KeyPointClassifier(
            model_path='hand-gesture-recognition-mediapipe/model/keypoint_classifier/keypoint_classifier.tflite'
        )
        
        point_history_classifier = PointHistoryClassifier(
            model_path='hand-gesture-recognition-mediapipe/model/point_history_classifier/point_history_classifier.tflite'
        )
        
        # Load labels
        with open('hand-gesture-recognition-mediapipe/model/keypoint_classifier/keypoint_classifier_label.csv',
                  encoding='utf-8-sig') as f:
            keypoint_classifier_labels = [row[0] for row in csv.reader(f)]
        
        with open('hand-gesture-recognition-mediapipe/model/point_history_classifier/point_history_classifier_label.csv',
                  encoding='utf-8-sig') as f:
            point_history_classifier_labels = [row[0] for row in csv.reader(f)]
        
        print("Models loaded successfully!")
        print(f"Available gestures: {keypoint_classifier_labels}")
        print(f"Available finger movements: {point_history_classifier_labels}")
        
    except Exception as e:
        print(f"Error loading models: {e}")
        raise e

def process_hand_landmarks(image, hand_landmarks, handedness, point_history=None):
    """Process hand landmarks and return gesture recognition results"""
    # Calculate bounding rectangle
    brect = calc_bounding_rect(image, hand_landmarks)
    
    # Calculate landmark list
    landmark_list = calc_landmark_list(image, hand_landmarks)
    
    # Preprocess landmarks
    pre_processed_landmark_list = pre_process_landmark(landmark_list)
    
    # Hand sign classification
    hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
    gesture_label = keypoint_classifier_labels[hand_sign_id] if hand_sign_id < len(keypoint_classifier_labels) else "Unknown"
    
    # Finger gesture classification (if point history is provided)
    finger_gesture_id = 0
    finger_gesture_label = "None"
    if point_history is not None:
        pre_processed_point_history_list = pre_process_point_history(image, point_history)
        if len(pre_processed_point_history_list) == (16 * 2):  # history_length * 2
            finger_gesture_id = point_history_classifier(pre_processed_point_history_list)
            if finger_gesture_id < len(point_history_classifier_labels):
                finger_gesture_label = point_history_classifier_labels[finger_gesture_id]
    
    return {
        'gesture_id': hand_sign_id,
        'gesture_label': gesture_label,
        'hand_landmarks': landmark_list,
        'bounding_rect': brect,
        'handedness': handedness.classification[0].label,
        'finger_gesture_id': finger_gesture_id,
        'finger_gesture_label': finger_gesture_label
    }

def decode_base64_image(image_base64: str):
    """Decode base64 image to OpenCV format"""
    try:
        # Remove data URL prefix if present
        if 'data:image' in image_base64:
            image_base64 = image_base64.split(',')[1]
        
        # Decode base64
        image_bytes = base64.b64decode(image_base64)
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv.imdecode(image_array, cv.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Failed to decode image")
        
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

def encode_image_to_base64(image):
    """Encode OpenCV image to base64"""
    _, buffer = cv.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{image_base64}"

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Hand Gesture Recognition API",
        "version": "1.0.0",
        "available_gestures": keypoint_classifier_labels,
        "available_finger_movements": point_history_classifier_labels,
        "endpoints": {
            "/": "This information",
            "/health": "Health check",
            "/gestures": "Get list of available gestures",
            "/analyze-image": "Analyze uploaded image for hand gestures",
            "/process-base64": "Process base64 encoded image",
            "/config": "Get/Set analysis configuration"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": {
            "gesture_recognizer": gesture_recognizer is not None,
            "keypoint_classifier": keypoint_classifier is not None,
            "point_history_classifier": point_history_classifier is not None
        }
    }

@app.get("/gestures")
async def get_available_gestures():
    """Get list of available hand gestures and finger movements"""
    return {
        "hand_gestures": {
            str(i): label for i, label in enumerate(keypoint_classifier_labels)
        },
        "finger_movements": {
            str(i): label for i, label in enumerate(point_history_classifier_labels)
        }
    }

@app.post("/analyze-image", response_model=ProcessImageResponse)
async def analyze_image(file: UploadFile = File(...), include_visualization: bool = True):
    """Analyze uploaded image for hand gestures"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and decode image
        contents = await file.read()
        image_array = np.frombuffer(contents, dtype=np.uint8)
        image = cv.imdecode(image_array, cv.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Process image
        results = process_image_for_gestures(image, include_visualization)
        return ProcessImageResponse(**results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/process-base64", response_model=ProcessImageResponse)
async def process_base64_image(request: ProcessImageRequest):
    """Process base64 encoded image for hand gesture recognition"""
    try:
        # Decode image
        image = decode_base64_image(request.image_base64)
        
        # Process image
        results = process_image_for_gestures(
            image, 
            request.include_visualization,
            request.include_landmarks
        )
        
        return ProcessImageResponse(**results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

def process_image_for_gestures(image, include_visualization=True, include_landmarks=True):
    """Core function to process image and detect hand gestures"""
    if gesture_recognizer is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    # Convert BGR to RGB
    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    rgb_image.flags.writeable = False
    
    # Process with MediaPipe
    results = gesture_recognizer.process(rgb_image)
    
    # Convert back to BGR for OpenCV
    rgb_image.flags.writeable = True
    debug_image = cv.cvtColor(rgb_image, cv.COLOR_RGB2BGR) if include_visualization else None
    
    detected_hands = []
    
    if results.multi_hand_landmarks is not None:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Process hand landmarks
            hand_result = process_hand_landmarks(image, hand_landmarks, handedness)
            
            gesture_result = GestureResult(
                gesture_id=hand_result['gesture_id'],
                gesture_label=hand_result['gesture_label'],
                hand_landmarks=hand_result['hand_landmarks'] if include_landmarks else None,
                bounding_rect=hand_result['bounding_rect']
            )
            
            detected_hands.append(gesture_result)
            
            # Add visualizations if requested
            if include_visualization and debug_image is not None:
                debug_image = draw_bounding_rect(True, debug_image, hand_result['bounding_rect'])
                debug_image = draw_landmarks(debug_image, hand_result['hand_landmarks'])
                debug_image = draw_info_text(
                    debug_image,
                    hand_result['bounding_rect'],
                    handedness,
                    hand_result['gesture_label'],
                    hand_result['finger_gesture_label']
                )
    
    response_data = {
        "detected_hands": detected_hands,
    }
    
    if include_visualization and debug_image is not None:
        response_data["processed_image_base64"] = encode_image_to_base64(debug_image)
    
    return response_data

@app.get("/config", response_model=AnalysisConfig)
async def get_config():
    """Get current analysis configuration"""
    return analysis_config

@app.post("/config", response_model=AnalysisConfig)
async def update_config(config: AnalysisConfig):
    """Update analysis configuration and reinitialize MediaPipe"""
    global analysis_config, gesture_recognizer
    
    try:
        analysis_config = config
        
        # Reinitialize MediaPipe with new config
        mp_hands = mp.solutions.hands
        gesture_recognizer = mp_hands.Hands(
            static_image_mode=config.use_static_image_mode,
            max_num_hands=config.max_num_hands,
            min_detection_confidence=config.min_detection_confidence,
            min_tracking_confidence=config.min_tracking_confidence,
        )
        
        return analysis_config
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating configuration: {str(e)}")

@app.get("/model-info")
async def get_model_info():
    """Get information about loaded models"""
    model_files = {
        "keypoint_classifier": "hand-gesture-recognition-mediapipe/model/keypoint_classifier/keypoint_classifier.tflite",
        "point_history_classifier": "hand-gesture-recognition-mediapipe/model/point_history_classifier/point_history_classifier.tflite"
    }
    
    model_info = {}
    for name, path in model_files.items():
        if os.path.exists(path):
            stat = os.stat(path)
            model_info[name] = {
                "path": path,
                "size_bytes": stat.st_size,
                "exists": True
            }
        else:
            model_info[name] = {
                "path": path,
                "exists": False
            }
    
    return {
        "models": model_info,
        "labels": {
            "gestures": keypoint_classifier_labels,
            "finger_movements": point_history_classifier_labels
        },
        "current_config": analysis_config
    }

@app.post("/batch-analyze")
async def batch_analyze_images(
    files: List[UploadFile] = File(...),
    include_visualization: bool = Query(False, description="Include visualization for all images"),
    include_landmarks: bool = Query(True, description="Include hand landmarks in response")
):
    """Analyze multiple images at once for batch processing"""
    if len(files) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed per batch")
    
    results = []
    for i, file in enumerate(files):
        if not file.content_type.startswith('image/'):
            results.append({
                "filename": file.filename,
                "index": i,
                "error": "File must be an image",
                "detected_hands": []
            })
            continue
        
        try:
            contents = await file.read()
            image_array = np.frombuffer(contents, dtype=np.uint8)
            image = cv.imdecode(image_array, cv.IMREAD_COLOR)
            
            if image is None:
                results.append({
                    "filename": file.filename,
                    "index": i,
                    "error": "Invalid image format",
                    "detected_hands": []
                })
                continue
            
            # Process image
            process_result = process_image_for_gestures(image, include_visualization, include_landmarks)
            
            results.append({
                "filename": file.filename,
                "index": i,
                "error": None,
                **process_result
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "index": i,
                "error": str(e),
                "detected_hands": []
            })
    
    return {
        "total_processed": len(files),
        "results": results
    }

class GestureStatistics(BaseModel):
    total_detections: int
    gesture_counts: Dict[str, int]
    most_common_gesture: Optional[str] = None
    detection_rate: float

@app.post("/analyze-with-stats", response_model=dict)
async def analyze_with_statistics(
    file: UploadFile = File(...),
    include_visualization: bool = True
):
    """Analyze image and return detection statistics"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        start_time = time.time()
        
        # Read and decode image
        contents = await file.read()
        image_array = np.frombuffer(contents, dtype=np.uint8)
        image = cv.imdecode(image_array, cv.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Process image
        results = process_image_for_gestures(image, include_visualization)
        
        processing_time = time.time() - start_time
        
        # Calculate statistics
        gesture_counts = {}
        for hand in results["detected_hands"]:
            label = hand.gesture_label
            gesture_counts[label] = gesture_counts.get(label, 0) + 1
        
        most_common = max(gesture_counts.items(), key=lambda x: x[1])[0] if gesture_counts else None
        
        stats = GestureStatistics(
            total_detections=len(results["detected_hands"]),
            gesture_counts=gesture_counts,
            most_common_gesture=most_common,
            detection_rate=len(results["detected_hands"]) / max(analysis_config.max_num_hands, 1)
        )
        
        return {
            **results,
            "statistics": stats.dict(),
            "processing_time_seconds": round(processing_time, 3),
            "image_dimensions": {
                "width": image.shape[1],
                "height": image.shape[0]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/demo-ui", response_class=HTMLResponse)
async def demo_ui():
    """Simple HTML demo interface for testing the API"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hand Gesture Recognition Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 800px; margin: 0 auto; }
            .result { margin: 20px 0; padding: 10px; border: 1px solid #ddd; }
            .processed-image { max-width: 100%; height: auto; }
            button { padding: 10px 20px; margin: 5px; }
            input[type="file"] { margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hand Gesture Recognition Demo</h1>
            
            <div>
                <h2>Upload Image</h2>
                <input type="file" id="imageInput" accept="image/*">
                <button onclick="analyzeImage()">Analyze Image</button>
                <button onclick="getGestures()">Get Available Gestures</button>
            </div>
            
            <div id="results"></div>
        </div>
        
        <script>
            async function analyzeImage() {
                const fileInput = document.getElementById('imageInput');
                const file = fileInput.files[0];
                
                if (!file) {
                    alert('Please select an image file');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', file);
                formData.append('include_visualization', 'true');
                
                try {
                    const response = await fetch('/analyze-image', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    displayResults(result);
                } catch (error) {
                    document.getElementById('results').innerHTML = 
                        `<div class="result">Error: ${error.message}</div>`;
                }
            }
            
            async function getGestures() {
                try {
                    const response = await fetch('/gestures');
                    const gestures = await response.json();
                    
                    let html = '<div class="result">';
                    html += '<h3>Available Gestures</h3>';
                    html += '<h4>Hand Gestures:</h4><ul>';
                    for (const [id, label] of Object.entries(gestures.hand_gestures)) {
                        html += `<li>${id}: ${label}</li>`;
                    }
                    html += '</ul><h4>Finger Movements:</h4><ul>';
                    for (const [id, label] of Object.entries(gestures.finger_movements)) {
                        html += `<li>${id}: ${label}</li>`;
                    }
                    html += '</ul></div>';
                    
                    document.getElementById('results').innerHTML = html;
                } catch (error) {
                    document.getElementById('results').innerHTML = 
                        `<div class="result">Error: ${error.message}</div>`;
                }
            }
            
            function displayResults(result) {
                let html = '<div class="result">';
                html += `<h3>Detection Results (${result.detected_hands.length} hands detected)</h3>`;
                
                result.detected_hands.forEach((hand, index) => {
                    html += `<div>`;
                    html += `<h4>Hand ${index + 1}: ${hand.gesture_label} (ID: ${hand.gesture_id})</h4>`;
                    html += `<p>Bounding box: [${hand.bounding_rect.join(', ')}]</p>`;
                    html += `</div>`;
                });
                
                if (result.processed_image_base64) {
                    html += `<img src="${result.processed_image_base64}" class="processed-image" alt="Processed image">`;
                }
                
                html += '</div>';
                document.getElementById('results').innerHTML = html;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/performance-test")
async def performance_test():
    """Test endpoint performance and model loading times"""
    start_time = time.time()
    
    # Test model availability
    models_available = {
        "gesture_recognizer": gesture_recognizer is not None,
        "keypoint_classifier": keypoint_classifier is not None,
        "point_history_classifier": point_history_classifier is not None
    }
    
    # Test with a simple synthetic image
    test_image = np.ones((400, 400, 3), dtype=np.uint8) * 128  # Gray image
    
    try:
        # Run a quick test detection
        test_results = process_image_for_gestures(test_image, include_visualization=False, include_landmarks=False)
        test_successful = True
    except Exception as e:
        test_successful = False
        test_results = {"error": str(e)}
    
    end_time = time.time()
    
    return {
        "performance_test": {
            "total_time_seconds": round(end_time - start_time, 3),
            "models_loaded": models_available,
            "test_detection_successful": test_successful,
            "test_results": test_results,
            "available_gestures_count": len(keypoint_classifier_labels),
            "available_movements_count": len(point_history_classifier_labels)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
