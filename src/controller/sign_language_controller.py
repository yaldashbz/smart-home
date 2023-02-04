import os
import string

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import mediapipe as mp
from keras.models import load_model
import numpy as np
import time
import pandas as pd
from base import BaseController


class SignLanguageController(BaseController):
    def __init__(self):
        self.model = load_model('../../models/sign_language_cnn.h5')

        mphands = mp.solutions.hands
        self.hands = mphands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        self.letterpred = list(string.ascii_uppercase)

    def process(self, img):
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
                print("Predicted Character 1: ", key)
                print('Confidence 1: ', 100 * value)
            elif value == high2:
                print("Predicted Character 2: ", key)
                print('Confidence 2: ', 100 * value)
            elif value == high3:
                print("Predicted Character 3: ", key)
                print('Confidence 3: ', 100 * value)
        time.sleep(5)

        framergb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.hands.process(framergb)
        hand_landmarks = result.multi_hand_landmarks
        if hand_landmarks:
            for handLMs in hand_landmarks:
                x_max = 0
                y_max = 0
                x_min = w
                y_min = h
                for lm in handLMs.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
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
                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.imshow("Frame", img)
