import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import mediapipe as mp
from keras.models import load_model
import numpy as np
import pandas as pd


class SignLanguageController:
    """Uses deep pre-trained model for detecting sign languages"""
    def __init__(self):
        self.model = load_model('../models/sign_language_cnn.h5')

        mphands = mp.solutions.hands
        self.hands = mphands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        self.letterpred = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                           'T', 'U', 'V',
                           'W', 'X', 'Y']

    def process(self, img):
        high_index = 0
        h, w, c = img.shape
        analysisframe = img
        showframe = analysisframe
        cv2.imshow("Frame", showframe)
        framergbanalysis = cv2.cvtColor(analysisframe, cv2.COLOR_BGR2RGB)
        resultanalysis = self.hands.process(framergbanalysis)
        hand_landmarksanalysis = resultanalysis.multi_hand_landmarks
        if hand_landmarksanalysis:
            for handLMsanalysis in hand_landmarksanalysis:
                x_max = 0
                y_max = 0
                x_min = w
                y_min = h
                for lmanalysis in handLMsanalysis.landmark:
                    x, y = int(lmanalysis.x * w), int(lmanalysis.y * h)
                    if x > x_max:
                        x_max = x
                    if x < x_min:
                        x_min = x
                    if y > y_max:
                        y_max = y
                    if y < y_min:
                        y_min = y
                y_min -= 20
                y_max += 20
                x_min -= 20
                x_max += 20

            analysisframe = cv2.cvtColor(analysisframe, cv2.COLOR_BGR2GRAY)
            analysisframe = analysisframe[y_min:y_max, x_min:x_max]
            analysisframe = cv2.resize(analysisframe, (28, 28))

            nlist = []
            rows, cols = analysisframe.shape
            for i in range(rows):
                for j in range(cols):
                    k = analysisframe[i, j]
                    nlist.append(k)

            datan = pd.DataFrame(nlist).T
            colname = []
            for val in range(784):
                colname.append(val)
            datan.columns = colname

            pixeldata = datan.values
            pixeldata = pixeldata / 255
            pixeldata = pixeldata.reshape(-1, 28, 28, 1)
            prediction = self.model.predict(pixeldata)
            predarray = np.array(prediction[0])
            letter_prediction_dict = {self.letterpred[i]: predarray[i] for i in range(len(self.letterpred))}
            predarrayordered = sorted(predarray, reverse=True)
            high1 = predarrayordered[0]
            high2 = predarrayordered[1]
            high3 = predarrayordered[2]
            for key, value in letter_prediction_dict.items():
                if value == high1:
                    high_index = self.letterpred.index(key)
                    print("Predicted Character 1: ", key)
                    print('Confidence 1: ', 100 * value)
                elif value == high2:
                    print("Predicted Character 2: ", key)
                    print('Confidence 2: ', 100 * value)
                elif value == high3:
                    print("Predicted Character 3: ", key)
                    print('Confidence 3: ', 100 * value)
        return high_index
