# Scripts and processes used for extracting book data in the yellow zone

import os
from cv2 import cv2
from langoon import extract_section_coordinates_from_image, crop_section_from_image, extract_dimensions_from_image

# The threshold breakpoint where an object is detected from its white background (value 0-255)
THRESHOLD_BREAKPOINT = 100
# The convertion metric used for detecting the physical dimension of an image
PIXELS_PER_METRIC = 130
# The amount of pixels to crop from the cover image to get sharper edges
CROP = 10

print("Opening 'example.jpg'")

# image = capture_camera_image()

image = cv2.imread("./tests/example.jpg")
coordinates = extract_section_coordinates_from_image(image, THRESHOLD_BREAKPOINT)
image = crop_section_from_image(image, coordinates, CROP)
height, width = extract_dimensions_from_image(image, PIXELS_PER_METRIC)

print("Height: ", height)
print("Width: ", width)

print("Saving 'optimized-example.jpg'")

cv2.imwrite("optimized-example.jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])