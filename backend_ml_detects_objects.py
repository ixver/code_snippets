
import numpy as np

def load_classnames(path):

    with open(path,'r') as f:
        classNames = f.read().rstrip('\n').split('\n')

    # check
    # print('\n classnames:',classNames)
    return classNames

def set_netData(cv2, frame):

    height, width, channels = frame.shape

    # prepare to feed image data into network
    # set image as blob, input image, forward image to output layers
    imgSizeA = 416
    imgSizeB = 416
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (imgSizeA, imgSizeB), swapRB=True, crop=False)

    # set detection parameters
    confidenceMinimum = 0.4
    iouThreshold = 0.5

    netData = {
        'blob': blob,
        'width': width,
        'height': height,
        'channels': channels,
        'confidenceMinimum': confidenceMinimum,
        'iouThreshold': iouThreshold,
    }

    return netData

def run_net(cv2, frame, net, classNames, netData, state):

    # initialize
    blob = netData['blob']
    width = netData['width']
    height = netData['height']
    confidenceMinimum = netData['confidenceMinimum']
    iouThreshold = netData['iouThreshold']

    # SET DETECTIONS
    # gets the output layers
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    # get aligned lists of detected object types
    class_ids = []
    confidences = []
    boxes = []
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidenceMinimum:

                # center x, y
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)

                # width
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # box x, y parameters
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # Non-maximum Suppression (NMS) sets minimum confidence and IOU threshold of overlapping proposals to shift to another list,
    ## avoiding multiple overlapping redundant boxes
    # IOU (Intersection over Union) calculation is actually used to measure the overlap between two proposals
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidenceMinimum, iouThreshold)

    # SET GRAPHICS
    colors = state['colors']
    fonttype = cv2.FONT_HERSHEY_PLAIN
    fontscale = 2.8
    fontthickness = 2
    if (colors is None):
        colorsArr = np.random.uniform(0, 255, size=(len(classNames), 3))
        colors = {}
        for i, cN in enumerate(classNames):
            colors[cN] = colorsArr[i].copy()

    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            classname = classNames[class_ids[i]]
            label = str(classname)
            confidence = str(round(confidences[i], 2))
            color = colors[classname]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + confidence, (x, y+48), fonttype, fontscale, color, fontthickness)

    # # CHECK
    # cv2.imshow("Image", frame)

    state['colors'] = colors
    return [frame, state]

def set_netdetection_general(cv2, frame, state):
    net = cv2.dnn.readNetFromDarknet('./models/yolov3.cfg', './models/yolov3.weights')
    path = './models/coco.names'
    classNames = load_classnames(path)

    netData = set_netData(cv2, frame)
    frame, _data = run_net(cv2, frame, net, classNames, netData, state)
    return [frame, state]


