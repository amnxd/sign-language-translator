#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Startup script for Hand Gesture Recognition FastAPI Server

This script provides an easy way to start the server with different configurations.
"""
import argparse
import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if required files and dependencies exist"""
    print("🔍 Checking requirements...")
    
    # Check if hand-gesture-recognition-mediapipe directory exists
    if not os.path.exists("hand-gesture-recognition-mediapipe"):
        print("❌ hand-gesture-recognition-mediapipe directory not found!")
        print("   Please ensure the hand-gesture-recognition-mediapipe module is in the current directory.")
        return False
    
    # Check if model files exist
    model_files = [
        "hand-gesture-recognition-mediapipe/model/keypoint_classifier/keypoint_classifier.tflite",
        "hand-gesture-recognition-mediapipe/model/point_history_classifier/point_history_classifier.tflite"
    ]
    
    missing_models = []
    for model_file in model_files:
        if not os.path.exists(model_file):
            missing_models.append(model_file)
    
    if missing_models:
        print("❌ Missing model files:")
        for model in missing_models:
            print(f"   - {model}")
        return False
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ main.py not found!")
        return False
    
    print("✅ All requirements satisfied!")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_server(host="0.0.0.0", port=8000, reload=False, workers=1):
    """Start the FastAPI server"""
    print(f"🚀 Starting Hand Gesture Recognition API Server...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Reload: {reload}")
    print(f"   Workers: {workers}")
    print()
    
    cmd = [
        sys.executable, "-m", "uvicorn", "main:app",
        "--host", host,
        "--port", str(port)
    ]
    
    if reload:
        cmd.append("--reload")
    else:
        cmd.extend(["--workers", str(workers)])
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Server shutdown requested by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Hand Gesture Recognition FastAPI Server Startup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_server.py                    # Start with default settings
  python start_server.py --dev             # Start in development mode with auto-reload
  python start_server.py --port 9000       # Start on port 9000
  python start_server.py --install         # Install dependencies and start
  python start_server.py --check-only      # Only check requirements
        """
    )
    
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind (default: 8000)")
    parser.add_argument("--dev", action="store_true", help="Development mode with auto-reload")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker processes (default: 1)")
    parser.add_argument("--install", action="store_true", help="Install dependencies before starting")
    parser.add_argument("--check-only", action="store_true", help="Only check requirements, don't start server")
    
    args = parser.parse_args()
    
    print("🤚 Hand Gesture Recognition FastAPI Server")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    if args.check_only:
        print("✅ Requirements check completed successfully!")
        return
    
    # Install dependencies if requested
    if args.install:
        if not install_dependencies():
            sys.exit(1)
    
    # Start server
    reload = args.dev
    workers = 1 if reload else args.workers  # uvicorn doesn't support multiple workers with reload
    
    print()
    print("🌐 Server will be available at:")
    print(f"   • Main API: http://{args.host}:{args.port}")
    print(f"   • Documentation: http://{args.host}:{args.port}/docs")
    print(f"   • Interactive Demo: http://{args.host}:{args.port}/demo-ui")
    print(f"   • Alternative Docs: http://{args.host}:{args.port}/redoc")
    print()
    
    start_server(args.host, args.port, reload, workers)

if __name__ == "__main__":
    main()
