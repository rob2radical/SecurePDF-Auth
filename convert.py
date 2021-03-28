import cv2
import imutils
import matplotlib.pyplot
from pdf2image import convert_from_path
from skimage.metrics import structural_similarity as ssim
import numpy


def remove_white_space(im):
    gray_color = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.cvtColor(gray_color, (25, 25), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV +
                           cv2.THRESH_OTSU)[1]

    noise_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, noise_kernel, iterations=2)
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, close_kernel, iterations=3)

    cords = cv2.findNonZero(close)
    x, y, w, h = cv2.boundingRect(cords)
    return image[y:y + h, x:x + w]


image = convert_from_path('Dependent Verification Form.pdf')

for i in image:
    i = numpy.array(i)
    ratio = i.shape[0] / 500.0
    matplotlib.pyplot.imshow(imutils.resize(i, height=1000))

i = numpy.array(image[-1])
original = i.copy()
ratio = i.shape[0] / 500.0
i = imutils.resize(i, height=500)
origin = i.copy()

gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

matplotlib.pyplot.imshow(gray, 'gray')
edged = cv2.Canny(gray, 80, 200)
matplotlib.pyplot.imshow(edged, 'gray')

cnt = cv2.findContours(edged.copy(), cv2.RETR_LIST,
                        cv2.CHAIN_APPROX_SIMPLE)
cnt = imutils.grab_contours(cnt)
cnt = sorted(cnt, key=cv2.contourArea, reverse=True)[:1]
for c in cnt:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.2 * peri, True)
    x, y, w, h = cv2.boundingRect(approx)
    cv2.rectangle(origin, (x, y), (x + w, y + h), (255, 0, 0), 2)
matplotlib.pyplot.imshow(origin)
remove_white_space(origin)

pic = cv2.cvtColor(cv2.imread('sample_2.png'), cv2.COLOR_BGR2RGB)
wrong_image = cv2.resize(cv2.cvtColor(pic.copy(), cv2.COLOR_BGR2GRAY), (100, 100))
original_image = cv2.resize(cv2.cvtColor(cropped_image.copy(), cv2.COLOR_BGR2GRAY), (100, 100))

print(ssim(original_image, original_image))
print(ssim(original_image, wrong_image))
