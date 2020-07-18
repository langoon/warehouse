# A shared Langoon library of utility functions used for extracting an processing book metadata

import numpy
from cv2 import cv2

def order_coordinates(coordinates):
  # Returns a list of coordinates that will be ordered
  # such that the first entry in the list is the top-left,
  # the second entry is the top-right, the third is the
  # bottom-right, and the fourth is the bottom-left

  # Sum and difference between the coordinates
  coordinates_sum = coordinates.sum(axis=1)
  coordinates_diff = numpy.diff(coordinates, axis=1)

  # Return ordered rectangle coordinates
  return numpy.array([
    # Top-left
    coordinates[numpy.argmin(coordinates_sum)],
    # Top-right
    coordinates[numpy.argmin(coordinates_diff)],
    # Bottom-right
    coordinates[numpy.argmax(coordinates_sum)],
    # Bottom-left
    coordinates[numpy.argmax(coordinates_diff)]
  ], dtype="float32")

def extract_dimensions_from_image(image, pixels_per_metric):
  # Takes an image and calculate its width and height based on a metric
  # The metric represents the number of pixels a mm, cm, inch, etc. takes up in the image

  # Get image dimensions
  image_height, image_width = image.shape[:2]

  # Convert px dimensions into the metric value and return the height and width in that value
  return image_height / (image_width / pixels_per_metric), image_width / (image_width / pixels_per_metric)

def crop_section_from_image(image, coordinates, crop):
  # Takes the coordinates for a rectangular polygon's location on an image,
  # orders those coordinates into a stright rectangle, and warps the image to fit those coordinates,
  # crops that section and returns it back

  source_rectangle = order_coordinates(coordinates)
  (tl, tr, br, bl) = source_rectangle

  # Compute the width of the new rectangle, which will be the
  # maximum distance between bottom-right and bottom-left
  # x-coordiates or the top-right and top-left x-coordinates
  max_width = max(
    int(numpy.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))),
    int(numpy.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2)))
  )

  # Compute the height of the new rectangle, which will be the
  # maximum distance between the top-right and bottom-right
  # y-coordinates or the top-left and bottom-left y-coordinates
  max_height = max(
    int(numpy.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))),
    int(numpy.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2)))
  )

  target_rectangle = numpy.array([
    # Top-left
    [ 0, 0 ],
    # Top-right
    [ max_width - 1, 0 ],
    # Bottom-right
    [ max_width - 1, max_height - 1 ],
    # Bottom-left
    [ 0, max_height - 1 ]
  ], dtype="float32")

  # Compute the perspective transform matrix
  matrix = cv2.getPerspectiveTransform(source_rectangle, target_rectangle)
  # Apply that transform matrix to the image
  image = cv2.warpPerspective(image, matrix, (max_width, max_height))
  # Crop the edges of the image and return it
  return image[ crop: -crop, crop: -crop ]

def extract_section_coordinates_from_image(image, threshold_breakpoint):
  # Takes an raw image with a white bright background and looks for the contour of 
  # a rectangular object and returns the coordinates representing a polygon shape of that object.
  # A threshold needs to be provided representing an acceptable breaking point at which the coordinates will be returned

  # The width of the border to wrap the image in case the object overflows the image
  BORDER_WIDTH = 100

  image = cv2.copyMakeBorder(image, BORDER_WIDTH, BORDER_WIDTH, BORDER_WIDTH, BORDER_WIDTH, cv2.BORDER_CONSTANT, value=[255, 255, 255])
  image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Calculate the image area
  image_height, image_width = image.shape[:2]
  image_area = image_height * image_width
  # Repeat to find the right threshold value for finding a rectangle
  found = False 
  # Increment the threshold until a contour is found
  threshold_current = threshold_breakpoint
  while found == False:
    if threshold_breakpoint < 200:
      threshold_breakpoint = threshold_current + 5
      threshold_current = threshold_breakpoint
    # Extract contours using threshold
    _, threshold = cv2.threshold(image_grayscale, threshold_breakpoint, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # Go through each contour that could be extracted from the image
    for contour in contours:
      contour_area = cv2.contourArea(contour)
      if contour_area > (image_area / 6) and contour_area < (image_area / 1.01):
        epsilon = 0.1 * cv2.arcLength(contour, True)
        # Close open lines into a complete wrapped shade
        approx = cv2.approxPolyDP(contour, epsilon, True)
        # When the shape can be wrapped the contour rectangle has been found
        if len(approx) == 4:
          found = True
        # Otherwise keep decrementing the threshold value until it's found
        else:
          threshold_breakpoint = threshold_breakpoint - 1
          break
        # Set and return coordinates from approximate
        coordinates = numpy.empty((4, 2), dtype="float32")
        # Top-left
        coordinates[0] = approx[0] - BORDER_WIDTH
        # Top-right
        coordinates[1] = approx[1] - BORDER_WIDTH
        # Bottom-right
        coordinates[2] = approx[2] - BORDER_WIDTH
        # Bottom-left
        coordinates[3] = approx[3] - BORDER_WIDTH
        return coordinates