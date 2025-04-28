import cv2
import time
import keyboard
from utils.hand_detector import HandDetector

def run_hill_climb():
    time.sleep(2.0)
    current_key_pressed = set()
    detector = HandDetector(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    video = cv2.VideoCapture(0)

    try:
        while True:
            key_pressed = False
            brake_pressed = False
            accelerate_pressed = False
            key_count = 0
            ret, image = video.read()
            if not ret:
                break

            image, fingers = detector.process_frame(image)
            if fingers:
                total = fingers.count(1)
                if total == 0:  # Closed fist -> Brake/Balance
                    cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, "BRAKE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    keyboard.press('left')
                    brake_pressed = True
                    current_key_pressed.add('left')
                    key_pressed = 'left'
                    key_count += 1
                elif total == 5:  # Open hand -> Accelerate
                    cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, "GAS", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    keyboard.press('right')
                    accelerate_pressed = True
                    current_key_pressed.add('right')
                    key_pressed = 'right'
                    key_count += 1

            if not key_pressed and current_key_pressed:
                for key in current_key_pressed:
                    keyboard.release(key)
                current_key_pressed.clear()
            elif key_count == 1 and len(current_key_pressed) == 2:
                for key in current_key_pressed:
                    if key_pressed != key:
                        keyboard.release(key)
                current_key_pressed = {key_pressed}

            cv2.imshow("Frame", image)
            if cv2.waitKey(1) == ord('q'):
                break

    finally:
        for key in current_key_pressed:
            keyboard.release(key)
        video.release()
        cv2.destroyAllWindows()