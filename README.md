# VisionAid Pro 👓

VisionAid Pro is a smart wearable system designed to assist visually impaired users in navigating environments safely using real-time object detection and tactile/audio feedback.

## 🚀 Tech Stack
- Raspberry Pi
- Python
- YOLO Object Detection
- HC-SR04 Ultrasonic Sensor
- Vibration Motor



## 🎯 Features
- Real-time object detection using camera
- Audio alerts and tactile feedback
- Edge computing using Raspberry Pi
- Designed to be compact and wearable

## 📚 EDI Capstone Project
70% hardware + 30% software  
Patent & Scopus journal publication in progress

## 📚 Project Documentation

- 📄 [System Architecture](./architecture.md)
- 📦 [Hardware Components List](./components_list.md)
- 🖼️ [Hardware Diagram](./hardware-flow.jpeg)


---

## 📁 Code Overview

The core code is inside the [`/code`](./code) folder.

## 📦 Prerequisites

Make sure the following packages and tools are installed on your Raspberry Pi:

- Python 3.7+
- [Ultralytics YOLOv8](https://docs.ultralytics.com/)
- OpenCV (`opencv-python`)
- `RPi.GPIO` (for GPIO control)
- `espeak` (for audio alerts)

You can install them using:

```bash
pip install ultralytics opencv-python
sudo apt-get install espeak

```markdown





To execute the object detection system, run:

```bash
python3 object_detection.py \
  --model runs/detect/train/weights/best.pt \
  --source usb0 \
  --thresh 0.5 \
  --inference_size 640x480 \
  --resolution 640x480 \
  --audio --audio-volume 80

