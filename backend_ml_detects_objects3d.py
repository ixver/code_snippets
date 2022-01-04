
import cv2
import mediapipe as mp
from xcv_general import *


def set_mpobjectron(state):
    if (state['mp_objectron'] is None):
        mp_objectron = mp.solutions.objectron
        state['mp_objectron'] = mp_objectron
    return state

def set_mpdrawing(state):
    if (state['mp_objectron'] is None):
        mp_drawing = mp.solutions.drawing_utils
        state['mp_drawing'] = mp_drawing
    return state

def apply_detection_objectron(cv2, frame, state):

    state = set_mpobjectron(state)
    state = set_mpdrawing(state)

    mp_objectron = state['mp_objectron']
    mp_drawing = state['mp_drawing']

    # OBJECTRON
    # out of box models available: camera, chair, cup, shoe
    classNames = ['Chair', 'Shoe', 'Camera', 'Cup']
    for cN in classNames:
        with mp_objectron.Objectron(static_image_mode=False,
                                    max_num_objects=6,
                                    min_detection_confidence=0.4,
                                    min_tracking_confidence=0.6,
                                    model_name=cN) as objectron:

            # convert for objectron
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False
            results = objectron.process(frame)

            # convert back for drawing
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if results.detected_objects:
                print('(detected)', end='  ')
                for detected_objects in results.detected_objects:

                    # process per detected object
                    mp_drawing.draw_landmarks(frame, detected_objects.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                    mp_drawing.draw_axis(frame, detected_objects.rotation, detected_objects.translation)

    showtitle = 'Objectron (MediaPipe)'
    cv2.imshow(showtitle, frame)
    return [frame, state]



