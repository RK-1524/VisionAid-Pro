import cv2, time, threading, argparse, subprocess
import RPi.GPIO as GPIO
from ultralytics import YOLO

# --- GPIO Setup ---
TRIG, ECHO, MOTOR = 23, 24, 18
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    for pin in [TRIG, MOTOR]: GPIO.setup(pin, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    GPIO.output(MOTOR, False)

def cleanup_gpio():
    GPIO.output(MOTOR, False)
    GPIO.cleanup()

# --- Measure Distance ---
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout = time.time() + 0.1
    while GPIO.input(ECHO) == 0 and time.time() < timeout: start = time.time()
    while GPIO.input(ECHO) == 1 and time.time() < timeout: end = time.time()

    return round((end - start) * 17150, 2) if end and start else -1

# --- Alerts ---
HARMFUL = {2, 3, 5, 7, 9, 11, 43, 76}
AUDIO_MSGS = {
    2: "Car detected", 3: "Motorcycle", 5: "Bus", 7: "Truck",
    9: "Traffic light", 11: "Stop sign", 43: "Knife", 76: "Scissors"
}
last_alert = {}
def speak(msg):
    subprocess.Popen(['espeak', '-a', '80', msg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def alert(class_id, distance):
    now = time.time()
    if class_id in last_alert and now - last_alert[class_id] < 3: return
    speak(AUDIO_MSGS[class_id])
    last_alert[class_id] = now

    if distance < 50: GPIO.output(MOTOR, True)
    elif distance < 100:
        GPIO.output(MOTOR, True); time.sleep(0.2)
        GPIO.output(MOTOR, False); time.sleep(0.1)
    elif distance < 200:
        GPIO.output(MOTOR, True); time.sleep(0.1)
        GPIO.output(MOTOR, False); time.sleep(0.3)
    else: GPIO.output(MOTOR, False)

# --- Distance Thread ---
distance = -1
def distance_thread():
    global distance
    while True:
        dist = measure_distance()
        if dist > 0: distance = dist
        time.sleep(0.1)

# --- Detection ---
def detect(model_path, cam_id, conf_thresh, inference_size):
    model = YOLO(model_path)
    cam = cv2.VideoCapture(0 if "picamera" in cam_id else int(cam_id.replace("usb", "")))

    while True:
        ret, frame = cam.read()
        if not ret: continue
        frame = cv2.resize(frame, inference_size) if inference_size else frame
        results = model(frame)[0]

        for box in results.boxes:
            cid = int(box.cls[0])
            if box.conf[0] < conf_thresh: continue
            if cid in AUDIO_MSGS:
                print(f"Detected: {AUDIO_MSGS[cid]}")
                alert(cid, distance)

# --- Main ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    parser.add_argument('--source', required=True)
    parser.add_argument('--thresh', type=float, default=0.6)
    parser.add_argument('--inference_size', default=None)
    args = parser.parse_args()

    setup_gpio()
    threading.Thread(target=distance_thread, daemon=True).start()

    try:
        size = tuple(map(int, args.inference_size.split('x'))) if args.inference_size else None
        detect(args.model, args.source, args.thresh, size)
    except KeyboardInterrupt:
        print("Exiting gracefully...")
    finally:
        cleanup_gpio()
# YOLO object detection code will go here
