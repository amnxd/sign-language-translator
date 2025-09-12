"""
Sign Language Translator GUI with Camera + Model Predictions
Requirements:
    pip install opencv-python pillow requests
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import requests
import base64
import threading
import time
import tensorflow.lite as tflite


# 🔗 Replace with your deployed model endpoint
# MODEL_ENDPOINT = "https://YOUR_MODEL_ENDPOINT/predict"

MODEL_ENDPOINT = "models/keypoint_classifier.tflite"


class SignLangApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Translator")
        self.root.configure(bg="black")

        self.cap = None
        self.running = False
        self.detecting = False
        self.frame_interval = 1.2  # seconds between predictions

        # UI Elements
        self.video_label = tk.Label(root, bg="black")
        self.video_label.pack(padx=10, pady=10)

        self.pred_label = tk.Label(root, text="Prediction: —", font=("Arial", 20, "bold"), fg="white", bg="black")
        self.pred_label.pack(pady=6)

        self.conf_label = tk.Label(root, text="Confidence: —", font=("Arial", 14), fg="gray", bg="black")
        self.conf_label.pack(pady=2)

        self.history_box = tk.Listbox(root, height=6, width=30, bg="black", fg="white", font=("Arial", 12))
        self.history_box.pack(pady=10)

        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="Start Camera", command=self.start_camera)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="Stop Camera", command=self.stop_camera)
        self.stop_btn.grid(row=0, column=1, padx=5)

        self.detect_btn = ttk.Button(btn_frame, text="Start Detection", command=self.start_detection)
        self.detect_btn.grid(row=0, column=2, padx=5)

        self.stop_detect_btn = ttk.Button(btn_frame, text="Stop Detection", command=self.stop_detection)
        self.stop_detect_btn.grid(row=0, column=3, padx=5)

    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.update_video()

    def stop_camera(self):
        self.running = False
        self.detecting = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.video_label.config(image="")

    def update_video(self):
        if self.running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

            self.root.after(30, self.update_video)

    def start_detection(self):
        if self.running and not self.detecting:
            self.detecting = True
            threading.Thread(target=self.detect_loop, daemon=True).start()

    def stop_detection(self):
        self.detecting = False

    def detect_loop(self):
        while self.detecting and self.cap:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # Encode frame to JPEG -> base64
            _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
            img_b64 = base64.b64encode(buffer).decode("utf-8")

            label, conf = "—", None
            try:
                res = requests.post(MODEL_ENDPOINT, json={"image_base64": img_b64}, timeout=8)
                if res.ok:
                    data = res.json()
                    top = data["predictions"][0] if "predictions" in data and data["predictions"] else None
                    if top:
                        label = top["label"]
                        conf = round(top["confidence"] * 100, 1)
                    else:
                        label = data.get("transcript", "—")
                else:
                    label = "ERR"
            except Exception:
                label = "ERR"

            # Update UI (thread-safe)
            self.root.after(0, self.update_prediction, label, conf)

            time.sleep(self.frame_interval)

    def update_prediction(self, label, conf):
        self.pred_label.config(text=f"Prediction: {label}")
        if conf is not None:
            self.conf_label.config(text=f"Confidence: {conf}%")
            self.history_box.insert(0, f"{label} ({conf}%)")
        else:
            self.conf_label.config(text="Confidence: —")
            self.history_box.insert(0, label)

        if self.history_box.size() > 10:
            self.history_box.delete(tk.END)

    def on_close(self):
        self.stop_camera()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SignLangApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
