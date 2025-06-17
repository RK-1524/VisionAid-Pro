# 🏗️ System Architecture - VisionAid Pro

The architecture of VisionAid Pro is modular and edge-compute focused, designed to operate without relying on cloud services for real-time responsiveness.

## 📐 Overview

1. **Camera Module** – Captures real-time video feed
2. **Raspberry Pi (Central Unit)** – Runs object detection using YOLO and processes sensor input
3. **Ultrasonic Sensor (HC-SR04)** – Measures distance from nearby obstacles
4. **YOLO Object Detection** – Identifies harmful objects like stairs, poles, etc.
5. **Output Modules**:
   - **Vibration Motor** – Tactile feedback
   - **Audio Module (Speaker/Buzzer)** – Voice alerts

## 🧠 Flow of Operation

1. Video + ultrasonic sensor input is fed into Raspberry Pi
2. YOLO runs inference on the camera feed
3. Depending on object and distance, appropriate feedback is triggered

---

> Designed for **real-time inference**, low-latency feedback, and **offline usability**.

