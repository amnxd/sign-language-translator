#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for Hand Gesture Recognition FastAPI
"""
import requests
import base64
import json
from pathlib import Path

# API Base URL
API_BASE = "http://localhost:8000"

def test_api_endpoints():
    """Test basic API endpoints"""
    print("Testing Hand Gesture Recognition API...")
    
    try:
        # Test root endpoint
        print("\n1. Testing root endpoint...")
        response = requests.get(f"{API_BASE}/")
        if response.status_code == 200:
            print("✓ Root endpoint working")
            data = response.json()
            print(f"Available gestures: {data.get('available_gestures', [])}")
        else:
            print(f"✗ Root endpoint failed: {response.status_code}")
    
        # Test health check
        print("\n2. Testing health check...")
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            health_data = response.json()
            print(f"Models loaded: {health_data.get('models_loaded', {})}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
    
        # Test gestures endpoint
        print("\n3. Testing gestures endpoint...")
        response = requests.get(f"{API_BASE}/gestures")
        if response.status_code == 200:
            print("✓ Gestures endpoint working")
            gestures = response.json()
            print(f"Hand gestures: {gestures.get('hand_gestures', {})}")
            print(f"Finger movements: {gestures.get('finger_movements', {})}")
        else:
            print(f"✗ Gestures endpoint failed: {response.status_code}")
    
        # Test model info
        print("\n4. Testing model info...")
        response = requests.get(f"{API_BASE}/model-info")
        if response.status_code == 200:
            print("✓ Model info endpoint working")
            model_info = response.json()
            print(f"Models exist: {[k for k, v in model_info['models'].items() if v.get('exists')]}")
        else:
            print(f"✗ Model info endpoint failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"✗ Error testing API: {e}")

def test_image_processing():
    """Test image processing with a sample image"""
    print("\n5. Testing image processing...")
    
    # Create a simple test image (white square with some content)
    import numpy as np
    import cv2 as cv
    
    # Create test image
    test_image = np.ones((400, 400, 3), dtype=np.uint8) * 255
    cv.putText(test_image, "Test Hand Image", (50, 200), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    # Encode to base64
    _, buffer = cv.imencode('.jpg', test_image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    try:
        # Test base64 processing
        payload = {
            "image_base64": f"data:image/jpeg;base64,{image_base64}",
            "include_landmarks": True,
            "include_visualization": True
        }
        
        response = requests.post(f"{API_BASE}/process-base64", json=payload)
        if response.status_code == 200:
            print("✓ Base64 image processing working")
            result = response.json()
            print(f"Detected hands: {len(result.get('detected_hands', []))}")
        else:
            print(f"✗ Base64 processing failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"✗ Error testing image processing: {e}")

def test_advanced_features():
    """Test advanced features like performance test and demo UI"""
    print("\n6. Testing advanced features...")
    
    try:
        # Test performance endpoint
        print("\n   Testing performance test...")
        response = requests.get(f"{API_BASE}/performance-test")
        if response.status_code == 200:
            print("✓ Performance test working")
            perf_data = response.json()
            print(f"Test completed in {perf_data['performance_test']['total_time_seconds']}s")
            print(f"Test detection successful: {perf_data['performance_test']['test_detection_successful']}")
        else:
            print(f"✗ Performance test failed: {response.status_code}")
    
        # Test demo UI endpoint
        print("\n   Testing demo UI...")
        response = requests.get(f"{API_BASE}/demo-ui")
        if response.status_code == 200:
            print("✓ Demo UI endpoint working")
            print("Demo UI available at: http://localhost:8000/demo-ui")
        else:
            print(f"✗ Demo UI failed: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error testing advanced features: {e}")

def test_statistics_endpoint():
    """Test the statistics endpoint with a sample image"""
    print("\n7. Testing statistics endpoint...")
    
    import numpy as np
    import cv2 as cv
    import io
    
    # Create test image
    test_image = np.ones((400, 400, 3), dtype=np.uint8) * 255
    cv.putText(test_image, "Statistics Test", (50, 200), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    # Convert to bytes for file upload simulation
    _, buffer = cv.imencode('.jpg', test_image)
    
    try:
        # Test statistics endpoint
        files = {'file': ('test_image.jpg', io.BytesIO(buffer.tobytes()), 'image/jpeg')}
        response = requests.post(f"{API_BASE}/analyze-with-stats", files=files)
        
        if response.status_code == 200:
            print("✓ Statistics endpoint working")
            result = response.json()
            stats = result.get('statistics', {})
            print(f"Processing time: {result.get('processing_time_seconds', 0)}s")
            print(f"Total detections: {stats.get('total_detections', 0)}")
            print(f"Image dimensions: {result.get('image_dimensions', {})}")
        else:
            print(f"✗ Statistics endpoint failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"✗ Error testing statistics endpoint: {e}")

def test_configuration():
    """Test configuration endpoints"""
    print("\n8. Testing configuration endpoints...")
    
    try:
        # Get current config
        response = requests.get(f"{API_BASE}/config")
        if response.status_code == 200:
            print("✓ Get config working")
            config = response.json()
            print(f"Current config: min_detection_confidence={config.get('min_detection_confidence')}")
        else:
            print(f"✗ Get config failed: {response.status_code}")
        
        # Test updating config
        new_config = {
            "min_detection_confidence": 0.8,
            "min_tracking_confidence": 0.6,
            "max_num_hands": 2,
            "use_static_image_mode": False
        }
        
        response = requests.post(f"{API_BASE}/config", json=new_config)
        if response.status_code == 200:
            print("✓ Update config working")
            updated_config = response.json()
            print(f"Updated config: min_detection_confidence={updated_config.get('min_detection_confidence')}")
        else:
            print(f"✗ Update config failed: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error testing configuration: {e}")

if __name__ == "__main__":
    test_api_endpoints()
    test_image_processing()
    test_advanced_features()
    test_statistics_endpoint()
    test_configuration()
    
    print("\n" + "="*50)
    print("🎉 Comprehensive API Testing completed!")
    print("")
    print("📖 Available Resources:")
    print("• API Documentation: http://localhost:8000/docs")
    print("• Interactive Demo: http://localhost:8000/demo-ui")
    print("• Alternative Docs: http://localhost:8000/redoc")
    print("")
    print("🚀 To start the server:")
    print("• Development: python main.py")
    print("• With reload: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
    print("• Production: uvicorn main:app --host 0.0.0.0 --port 8000")
