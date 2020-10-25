import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=True)
args = vars(ap.parse_args())

# reading image
image = cv2.imread(args["input"])

B = image[:, :, 0]
G = image[:, :, 1]
R = image[:, :, 2]##

gray = (0.3 * R + 0.59 * G + 0.11 * B)
gray = gray.astype(np.uint8)

cv2.imshow("Original", image)
cv2.imshow("GrayScale", gray)

cv2.waitKey(0)
cv2.destroyAllWindows()