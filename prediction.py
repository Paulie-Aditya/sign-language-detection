import pickle

import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import requests
from io import BytesIO

model_dict = pickle.load(open('./models/stacked_model_new.p', 'rb')) 

labels = ['A','B','C','D','E','F','G','H','I','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y']

model = model_dict['model']


# get url from backend

# def prediction(url):
#     response = requests.get(url)
#     print(response)
#     img = Image.open(BytesIO(response.content))
#     img.save('image.jpg')
#     #cap = cv2.VideoCapture(0)
def prediction():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.3)
    hands.maxHands = 1

    data_aux = []
    x_ = []
    y_ = []

    frame = cv2.imread('image.jpg')

    H,W, _ = frame.shape
    #print(response.content)
        #H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        if(len(results.multi_hand_landmarks) == 1):

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

            if(len(data_aux) == 42):
                prediction = model.predict([np.asarray(data_aux)])

                predicted_character = labels[prediction[0]]

                return predicted_character
                # cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                #             cv2.LINE_AA)
        else:

            return "Too many Hands"

# url = '''
# data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxASEhMSEhESEhMWExISEhERFxUTFRUSFRUWFxUSGBYYICkgGCYlHRMVITEhJSkrLi4uGB8zODMtNygtLisBCgo
# KDg0OFxAQGS0iHyUtKysrKystLSstLS0uLS0tLSstLS0tKy0tLSstLTctLSstLS0tKy0tLS0tKy0tLTc3Lf/AABEIALcBEwMBIgACEQEDEQH/xAAbAAEAAQUBAAAAAAAAAAAAAAAABAIDBQYHAf
# /EAD8QAAIBAgMEBwUFBAsAAAAAAAABAgMRBCExBRJBUQYTImFxgZEyQlKhsWJywdHhM0OSogcUFSRTY3OCssLw/8QAGQEBAAMBAQAAAAAAAAAAAAAAAAECAwQF/8QAIREBAQACAQQDAQ
# EAAAAAAAAAAAECEQMhMUFRBBITYRT/2gAMAwEAAhEDEQA/AOyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADw9NKxVOuqkqlKe7VhJqSekrPO64pmybL2xTrJK6hUt2qTeaa1t8S718imOe2ufFcevdkQAXZAAAAAA
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC1iK8ILenJRXN/wDsyDS6QYSTssRTvyk93/lYidLsDXq0r0O1JJ3hknJO2cW8r5aHJMVTq05NVYTpu+amnF/Mxz5Msb2dfD8fDkx3vq7tCpF6ST8GmV
# nCaGNnFZSf6G29HNtS6jtVJ712/aenIic3uJy+JZ2rZek+HnT/ALxBNrJVYrNpLSf4M1+O5XipRdne64NPVNMyuy9t1qk3GNTeSTlLeSdlyvbwKcXhbvrEoxb1UVup9/cytsvWNMZljPrkn7N2
# rVglGst+OnWL2195e946+JnaGIhNXhJSXc9PFcDW8FX3oWeV1lcgVI1FPepycJLSUfo+DXcy8zsY5cMv8bwDCbO2/GXZrJQlpvr2G/8Ar55d5mjWWVzXGzu9ABKAAAAAAAAAAAAAAAAAAAAAA
# AAAAAAAAAAGmf0gbRnTSj2lCUVutX3XK7um+drZGs7K6Y4qklFyVWN7bta87eEr38rnT9pYalUpThVipw3W5R8Fe65PvOSbSwlCM1GDlFa9p71r+V8jm5d43cr0fjXHPD62dmRxu1sJXa63BR
# i3l1mHn1clfi47tpa8SLU2bhl+zq4qkv8AMp06q/kmn8iNV2FiJJSpwdWKteVFqrpz3G2vMjV69WGU4zj95NfUztvlrJj4rbOh9ONPrF1saqlnvRjUg1ZZKSnFd+jfEm4jG27WqjJXXON8zFd
# HcbvUOzm+NreGfoVUZXk4vR318yfCNbttbH1lONnezsopcHbT6FudS92WaGFU4OMtYaP7PD8i06bg7fUtLpldVaxHgX6O1qmGV49qHGnLT/a/d+ncWppu+hiMZfhflmX/ALGWt9K6HsnadLEQ36
# b7pRftRfJr8SacrwM6tGSnTk4vu4rk1o0bbgOlLatUpq/ODt8n+ZbHknlllxWdmzggYXbFCppNRfKfZ+enzJxpLKyss7vQASgAAAAAAAAAAAAAAAAAAAAAAAAAAHhzbpf0VrQqOrQpudLVxhn
# KD4rd1t4XOlFFaG9GUb2vFq64XVrlc8ZlGvFy3ju44terSzalTlnZ3s/VaEzD9IsTupOvV04zk/k2RtqYiSqyjPtbvtJ3SfGUea5HsFg27OnWjdXShVjb+anl6nJHp5avXW0nZ+0p1JSbm3J5ZK
# Mb2vbKKXrqZTD0GruTt58TB4KnRp1l1XWJSvdVZQlw4bsUZl4l2ZKraqNHdlGSeTST8ybiMBCas+y+ZEw8m4Q+6tSa5SSyfqaac1rDYrY9RaNNc9DEbSoqC7Tz7mzcXWVs35Gu7Ypwk+BWpnXuw
# kJZWv8AoiRhoMojSja/e16E2jT0s7WWjI0Uh4E/CVqkPYnKPdqvR5Efc42JOHS4Eq92Uobamvbgn3xyfoyfQ2nRl76T5S7L+eT8jCSSLc6SLTksUvHK2pM9NVi5QzjJrwyJVHatZatS+8vyLzln
# lneK+GwAxVPbK96m191p/WxIhtSk/ea8U/wLzPG+VbhlPCaC1DEwek4vzRdLKaAAAAAAAAAAAAAAAAAAAAAGu9IuiOHxV526qt/ixWr+3HSXyfeahX/o8xqd41KE7ZJ704t37t38TqIKXCVrjzZ
# 49JXJa3Q7aUbNUoyafu1IaebRZq/1qkmquHrQtxcJW4+8lb5nYAmV/KLz5OXmOcQ6TUrRW8lkstC++kULZTN+qQUspJSXKST+pArbBwc3eWGoN8+rin8kPzvtP7z00ufSOnb2jD4/balozpNPo7
# go6YWh/BF/UrqbCwklZ4ahb/TgvoiPyvtP+ienMNmY66WfG7M9h66kZrGdB8K86O9Ql9l70POMvwaMLitjYrD5un1kF79K8vWPtL0t3lbjlEzkxyTKS5F6K/UwtHaS5mVwuKTRGyxIu13lyLyue
# Ka4HnEaPsrPUjw9hIrpKtUz3qyqLKrk6NrMqSKVBrRteDt9CQyhojSVMMTVX7yfm7/Uuxx9Ze9fxS/ItpHqiN1Gp6Xv7Tq/Z9P1Ba3AT9svaPpj6bCADqcgAAAAAAAAAAAAAAAAAAAAAAAAAAMf
# tHY2Hr/tKUXL412Z/wASz9TX8X0Vq086FTrF8FS0ZeUtH52NwBW4yrY52Ocyxk6ctyrGVOXKat6c/FEuhj0+Ju2Iw8Kkd2pCM4/DJKS+ZruP6HUnnQnKi/hd5w+buvXyKXC+Gs5Ze6PCsmXqbRh
# cXgMXh/bg5RX7yn2o25vivNI9wm0k+JTWmnS9meTK4sgU8UmSYVUEaqQUsb6PGwjYmVQKVE9RC21ywKN8Eo22AAHQ5QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxG0ujuGrXbh1c379O0Xfm1o/
# NGXAs2mWzs0fF9HMVSzptV493Zn/C9fJsx1Pabi3GacZLWMk4teKeZ0kjY3A0qy3atOM1w3lmvB6ryM7h6aTl9tOpbRT4olQxFy9jehsNaFRwfwVO1HwT1XncwuJwGLoftKUnFe/T7cfHLNeaRS
# 42NJljWajWKusMFh9oJ6Mn0aqfEhZkOsZ4WlUAQ2wAHQ5QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGNx+w8NWznTSl8cOxL1WvncweJ6LVoZ0aiqL4KnZl5SWT87G3ArcZVpnY0KUcT
# HJ4etda2g5L1WTPDfgV/Nf8AX+AANGQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/9k='''

# with open("url.txt", "rb") as url_file:
#     url = 
# url= "https://img.freepik.com/free-photo/reaching-female-hand_628469-419.jpg"
# print(prediction(url))