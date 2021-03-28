import numpy as np
import cv2
from PyQt5 import QtWidgets

drawing = False
mode = True
img = np.zeros((512, 512, 3), np.uint8)
img.fill(255)


def clearScreen():
    img.fill(255)


def draw_rec(event, former_x, former_y, flags, param):
    global current_former_x, current_former_y, drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        current_former_x, current_former_y = former_x, former_y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if mode:
                cv2.line(img, (current_former_x, current_former_y), (former_x, former_y), (0, 0, 0), 5)
                current_former_x = former_x
                current_former_y = former_y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode:
            cv2.line(img, (current_former_x, current_former_y), (former_x, former_y), (0, 0, 0), 5)
            current_former_x = former_x
            current_former_y = former_y
    return former_x, former_y


def signaturePad():
    cv2.namedWindow(winname="Signature")
    cv2.setMouseCallback("Signature", draw_rec)
    # cv2.createButton('X', clearScreen)
    while True:
        cv2.imshow("Signature", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        if cv2.getWindowProperty('Signature', 1) == -1:
            break

    # return the png here
    print("picture here")

    cv2.destroyAllWindows()
    img.fill(255)
