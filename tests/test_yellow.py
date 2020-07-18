import unittest
import os
import langoon
from cv2 import cv2

class TestLangoon(unittest.TestCase):

  def setUp(self):
    self.image = cv2.imread("./tests/example.jpg")

  def tearDown(self):
    if os.path.isfile("./tests/optimized-example.jpg"):
      os.remove("./tests/optimized-example.jpg")

  def test_extract_section_coordinates_from_image(self):
    coordinates = langoon.extract_section_coordinates_from_image(self.image, 100)
    self.assertEqual(coordinates[0][0], 2345.)
    self.assertEqual(coordinates[0][1], 780.)
    self.assertEqual(coordinates[1][0], 2405.)
    self.assertEqual(coordinates[1][1], 3118.)
    self.assertEqual(coordinates[2][0], 924.)
    self.assertEqual(coordinates[2][1], 3148.)
    self.assertEqual(coordinates[3][0], 795.)
    self.assertEqual(coordinates[3][1], 872.)

  def test_extract_dimensions_from_image(self):
    height, width = langoon.extract_dimensions_from_image(self.image, 100)
    self.assertEqual(height, 133.33333333333334)
    self.assertEqual(width, 100)
    height, width = langoon.extract_dimensions_from_image(self.image, 150)
    self.assertEqual(height, 200.0)
    self.assertEqual(width, 150)

  def test_crop_section_from_image(self):
    coordinates = langoon.extract_section_coordinates_from_image(self.image, 100)
    image = langoon.crop_section_from_image(self.image, coordinates, 10)
    height, width = langoon.extract_dimensions_from_image(image, 150)
    self.assertEqual(height, 226.95822454308095)
    self.assertEqual(width, 150)

if __name__ == '__main__':
    unittest.main()
