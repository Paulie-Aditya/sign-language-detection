import pickle

import cv2
import mediapipe as mp
import numpy as np

#model_dict = pickle.load(open('./model.p', 'rb')) # try different models here

#model_dict = pickle.load(open('./models/rf_model.p', 'rb')) 
# model_dict = pickle.load(open('./models/svm_model.p', 'rb')) 
# model_dict = pickle.load(open('./models/gb_model.p', 'rb')) 
# model_dict = pickle.load(open('./models/histgb_model.p', 'rb')) 
model_dict = pickle.load(open('./models/stacked_model_new.p', 'rb')) 

labels = ['A','B','C','D','E','F','G','H','I','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y']

model = model_dict['model']

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.3)
hands.maxHands = 1
#labels_dict = {0: 'A', 1: 'B', 2: 'L'}
while True:

    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

  
    # Start coordinate, here 
    # represents the top left corner of rectangle 
    start_point = (10, 10) 
    
    # Ending coordinate, here 
    # represents the bottom right corner of rectangle 
    end_point = (300,300) 
    
    # Blue color in BGR 
    color = (255, 0, 0) 
    
    # Line thickness of 2 px 
    thickness = 2
    
    # Using cv2.rectangle() method 
    # Draw a rectangle with blue line borders of thickness of 2 px 
    rect = cv2.rectangle(frame, start_point, end_point, color, thickness) 

    
    new_frame = frame.copy()
    new_frame = new_frame[10:300 , 10:300]
    H, W, _ = new_frame.shape
    frame_rgb = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        #hand_landmarks = results.multi_hand_landmarks[0]
        if(len(results.multi_hand_landmarks) == 1):
            # for hand_landmarks in results.multi_hand_landmarks:
            #     mp_drawing.draw_landmarks(
            #         new_frame,  # image to draw
            #         hand_landmarks,  # model output
            #         mp_hands.HAND_CONNECTIONS,  # hand connections
            #         mp_drawing_styles.get_default_hand_landmarks_style(),
            #         mp_drawing_styles.get_default_hand_connections_style())

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            if(len(data_aux) ==42):
                prediction = model.predict([np.asarray(data_aux)])

                predicted_character = labels[prediction[0]]
                #predicted_character = labels_dict[int(prediction[0])]

                #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                            cv2.LINE_AA)
        else:
            cv2.putText(frame, "Too Many Hands Present on Screen!", (100, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,243,255), 1)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)


cap.release()
cv2.destroyAllWindows()
