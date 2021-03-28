import numpy as np
import cv2

drawing = False
mode = True


def draw_rec(event, former_x, former_y, flags, param):
    global current_former_x, current_former_y, drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        current_former_x, current_former_y = former_x, former_y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if mode:
                cv2.line(img, (current_former_x, current_former_y), (former_x, former_y), (255, 255, 255), 5)
                current_former_x = former_x
                current_former_y = former_y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode:
            cv2.line(img, (current_former_x, current_former_y), (former_x, former_y), (255, 255, 255), 5)
            current_former_x = former_x
            current_former_y = former_y
    return former_x, former_y


img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow(winname='Signature')
cv2.setMouseCallback('Signature', draw_rec)
while True:
    cv2.imshow('Sign', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

    if cv2.getWindowProperty('Signature',cv2.WND_PROP_VISIBLE) == 0:
        break

cv2.destroyAllWindows()

# return the png here