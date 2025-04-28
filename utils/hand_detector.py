import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_hand = mp.solutions.hands
        self.hands = self.mp_hand.Hands(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.tip_ids = [4, 8, 12, 16, 20]
        # Custom drawing styles
        self.landmark_drawing_spec = self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=4, circle_radius=6)  # Green landmarks
        self.connection_drawing_spec = self.mp_draw.DrawingSpec(color=(255, 165, 0), thickness=3)  # Orange connections

    def process_frame(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lm_list = []
        fingers = []

        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                my_hands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(my_hands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
                self.mp_draw.draw_landmarks(
                    image, 
                    hand_landmark, 
                    self.mp_hand.HAND_CONNECTIONS,
                    self.landmark_drawing_spec,
                    self.connection_drawing_spec
                )

                if lm_list:
                    # Thumb
                    if lm_list[self.tip_ids[0]][1] > lm_list[self.tip_ids[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    # Other fingers
                    for id in range(1, 5):
                        if lm_list[self.tip_ids[id]][2] < lm_list[self.tip_ids[id] - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)

        return image, fingers

    def process_frame_with_landmarks(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lm_list = []
        fingers = []

        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                my_hands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(my_hands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
                self.mp_draw.draw_landmarks(
                    image, 
                    hand_landmark, 
                    self.mp_hand.HAND_CONNECTIONS,
                    self.landmark_drawing_spec,
                    self.connection_drawing_spec
                )

                if lm_list:
                    # Thumb
                    if lm_list[self.tip_ids[0]][1] > lm_list[self.tip_ids[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    # Other fingers
                    for id in range(1, 5):
                        if lm_list[self.tip_ids[id]][2] < lm_list[self.tip_ids[id] - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)

        return image, fingers, lm_list

    def close(self):
        self.hands.close()