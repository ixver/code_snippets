import math
import numpy as np
import mediapipe as mp
import cv2

from xdevices import *

#Initializations: static code
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

def get_hands_detector(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
    mpHands = mp.solutions.hands
    return mpHands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence)

def get_results(detector, image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # mediapipe needs RGB
    results = detector.process(image).multi_hand_landmarks
    return results

def get_lmpositions(results, img, indicesChosen):

    lmlist = []

    if results:
        for lmIndex, lmVals in enumerate(results):
            condx = False
            if (indicesChosen=='all') or (lmIndex in indicesChosen):
                condx = True

            if condx:

                myHand = results[lmIndex]
                for id, lm in enumerate(myHand.landmark):

                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    # for each landmark return [landmark number, xposition, yposition]
                    lmlist.append([id,cx,cy])

    return lmlist

def get_fingersUp(lmlist):

    # each landmark array values: [landmark number, xposition, yposition]
    fingers = []
    tipIds = [4, 8, 12, 16, 20]

    # thumb is out
    if lmlist[tipIds[0]][1] < lmlist[2][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # each 4 fingers is out
    for id in range(1, 5):
        if lmlist[tipIds[id]][2] < lmlist[tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def set_frame_canvas_merged(cv2, frameRaw, state):

    frameCanvas = state['frameCanvas']

    # set thresholds, use mask to set frame, canvas colors
    imgGray = cv2.cvtColor(frameCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    # cv2.imshow("Image", frameRaw)
    frameRaw = cv2.bitwise_and(frameRaw, imgInv)
    frameRaw = cv2.bitwise_or(frameCanvas, frameRaw)
    return frameRaw

def set_canvas_graphics(cv2, lmpositions_list, frameRaw, state):

    frameCanvas = state['frameCanvas']
    xp = state['xp']
    yp = state['yp']
    brushSize = state['brushSize']
    drawColor = state['drawColor']
    canvasW = state['canvasW']
    canvasH = state['canvasH']
    textColor = drawColor

    if (lmpositions_list):

        # GET DATA
        # xp, yp = [0, 0]
        indextip = 8
        x1, y1 = lmpositions_list[indextip][1:]
        if (x1<0):
            x1 = 0
        if (y1<0):
            y1 = 0
        fingersUp = get_fingersUp(lmpositions_list)

        # DRAW SCHEME
        label = ''

        # only index finger is up
        if fingersUp[1] and fingersUp[2]!=1 and fingersUp[3]!=1 and fingersUp[4]!=1 and fingersUp[0]!=1:

            # set current mode label
            label = 'drawing'

            # show brush set at finger
            cv2.circle(frameRaw, (x1, y1), brushSize, drawColor, cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # drawing the line
            if drawColor == (0, 0, 0):
                cv2.line(frameRaw, (xp, yp), (x1, y1), drawColor, brushSize)
                cv2.line(frameCanvas, (xp, yp), (x1, y1), drawColor, brushSize)
            else:
                cv2.line(frameRaw, (xp, yp), (x1, y1), drawColor, brushSize)
                cv2.line(frameCanvas, (xp, yp), (x1, y1), drawColor, brushSize)

            xp, yp = x1, y1

        # index and middle fingers
        elif fingersUp[1] and fingersUp[2] and fingersUp[3]!=1 and fingersUp[4]!=1 and fingersUp[0]!=1:

            # show brush set at finger
            cv2.circle(frameRaw, (x1, y1), brushSize, drawColor, cv2.FILLED)

            # set current mode label
            label = 'moving position...'

        # 3 fingers are up - control color
        elif fingersUp[1] and fingersUp[2] and fingersUp[3] and fingersUp[4]!=1 and fingersUp[0]!=1:

            # show brush set at finger
            cv2.circle(frameRaw, (x1, y1), brushSize, drawColor, cv2.FILLED)

            lineWeight = 11

            # SET COLOR VALUE WITH HAND LOCATION
            brushColor = np.array(drawColor)
            label = ''

            if y1 < round(state['canvasH']*1/3, 2):
                # RED
                # set current mode label
                label = 'setting red tint'
                textColor = (0,0,255)

                # show area outline
                cv2.rectangle(frameRaw, (0,0), (canvasW, int(canvasH/3)), (0,0,255,0.28), lineWeight) # bgr

                # set color
                brushColor[2] = int(np.interp(x1, [0, state['canvasW']], [0, 255]))

            elif (state['canvasH'] * 1 / 3) < y1 < (state['canvasH'] * 2 / 3):
                # GREEN
                # set current mode label
                label = 'setting green tint'
                textColor = (0,255,0)

                # show area outline
                cv2.rectangle(frameRaw, (0,int(canvasH/3)), (canvasW, int(canvasH*2/3)), (0,255,0,0.28), lineWeight) # bgr

                # set color
                brushColor[1] = int(np.interp(x1, [0, state['canvasW']], [0, 255]))

            elif (state['canvasH']*2/3) < y1:
                # BLUE
                # set current mode label
                label = 'setting blue tint'
                textColor = (255,0,0)

                # show area outline
                cv2.rectangle(frameRaw, (0,int(canvasH*2/3)), (canvasW, int(canvasH)), (255,0,0,0.28), lineWeight) # bgr

                # set color
                brushColor[0] = int(np.interp(x1, [0, state['canvasW']], [0, 255]))

            drawColor = tuple(brushColor.tolist())

        # 4 fingers are up - control brush size
        elif fingersUp[1] and fingersUp[2] and fingersUp[3] and fingersUp[4] and fingersUp[0]!=1:

            # set current mode label
            label = 'setting brush size'

            # show brush set at finger
            cv2.circle(frameRaw, (x1, y1), brushSize, drawColor, cv2.FILLED)

            # set brush size
            brushSize = int(np.interp(x1, [0, state['canvasW']], [0, 160]))

        # 5 fingers are up - erase
        elif fingersUp[1] and fingersUp[2] and fingersUp[3] and fingersUp[4] and fingersUp[0]:

            # set current mode label
            label = 'erasing...'

            # show brush set at finger
            cv2.circle(frameRaw, (x1, y1), brushSize, drawColor, cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # set to black as eraser
            cv2.line(frameRaw, (xp, yp), (x1, y1), (0,0,0,), brushSize)
            cv2.line(frameCanvas, (xp, yp), (x1, y1), (0,0,0,), brushSize)

            # save current position
            xp, yp = x1, y1

        # show current/selected draw configuration
        fonttype = cv2.FONT_HERSHEY_PLAIN
        fontscale = 2.8
        fontthickness = 4
        cv2.putText(frameRaw, label + " ", (28, canvasH-48), fonttype, fontscale, textColor, fontthickness)
        cv2.circle(frameRaw, (canvasW-88, canvasH-88), brushSize, drawColor, cv2.FILLED)

    state['frameCanvas'] = frameCanvas
    state['xp'] = xp
    state['yp'] = yp
    state['brushSize'] = brushSize
    state['drawColor'] = drawColor
    return [cv2, state]

def cap_intercept_drawSchemeB(cv2, frameRaw, state):

    # INITIALIZE
    # set initial data
    dataInitial = {
        'canvasW': 1280,
        'canvasH': 720,
        'xp': 0,
        'yp': 0,
        'brushThickness': 15,
        'eraserThickness': 50,
        'brushSize': 55,
        'drawColor': (255, 0, 0),
    }
    if (state is None):
        state = dataInitial
    else:
        for k, v in dataInitial.items():
            if k not in list(state.keys()):
                state[k] = v

    # set canvas
    if 'frameCanvas' not in list(state.keys()):
        state['frameCanvas'] = np.zeros((dataInitial['canvasH'], dataInitial['canvasW'], 3), np.uint8)

    # set handdetector
    if 'handdetector' in list(state.keys()):
        handDetector = state['handdetector']
    else:
        handDetector = get_hands_detector(min_detection_confidence=0.7)
        state['handdetector'] = handDetector

    # TRANSFORM
    # flip capture view/frame
    frameRaw = cv2.flip(frameRaw, 1)

    # get landmarks data
    results = get_results(handDetector, frameRaw)

    # get landmarks positions
    lmpositions_list = get_lmpositions(results, frameRaw, [0])

    # draw canvas/paint graphics, merge canvas/graphics with image
    cv2, state = set_canvas_graphics(cv2, lmpositions_list, frameRaw, state)
    frameRaw = set_frame_canvas_merged(cv2, frameRaw, state)

    # check images/captures
    # cv2.imshow("Image", frameRaw)
    # cv2.imshow("Canvas", frameCanvas)
    # cv2.imshow("Volume", frameRaw)

    return [frameRaw, state]

