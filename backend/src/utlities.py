import numpy as np
import cv2

def preprocess_image(img):
    # Convert image to grayscale
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
     # Resize the image with a scaling factor of 1.5
    resized = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    # Apply adaptive thresholding
    processed_image = cv2.adaptiveThreshold(resized,
                                            255,
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY,
                                            61,
                                            11)
    return processed_image