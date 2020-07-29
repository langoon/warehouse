import unittest
from commands.langoon import Image
from cv2 import cv2

class TestImage(Image, unittest.TestCase):

    def setUp(self):
        self.frontcover = cv2.imread("./tests/example_frontcover.jpg")

    def test_extract_section_coordinates_from_image(self):
        coordinates = self.extract_section_coordinates_from_image(self.frontcover, 100)
        self.assertEqual(coordinates[0][0], 2345.)
        self.assertEqual(coordinates[0][1], 780.)
        self.assertEqual(coordinates[1][0], 2405.)
        self.assertEqual(coordinates[1][1], 3118.)
        self.assertEqual(coordinates[2][0], 924.)
        self.assertEqual(coordinates[2][1], 3148.)
        self.assertEqual(coordinates[3][0], 795.)
        self.assertEqual(coordinates[3][1], 872.)

    def test_extract_dimensions_from_image(self):
        height, width = self.extract_dimensions_from_image(self.frontcover, 100)
        self.assertEqual(height, 133.33333333333334)
        self.assertEqual(width, 100)
        height, width = self.extract_dimensions_from_image(self.frontcover, 150)
        self.assertEqual(height, 200.0)
        self.assertEqual(width, 150)

    def test_crop_section_from_image(self):
        coordinates = self.extract_section_coordinates_from_image(self.frontcover, 100)
        image = self.crop_section_from_image(self.frontcover, coordinates, 10)
        height, width = self.extract_dimensions_from_image(image, 150)
        self.assertEqual(height, 226.95822454308095)
        self.assertEqual(width, 150)

    def test_extract_barcode_from_image(self):
        isbn_image = cv2.imread("./tests/example_barcode_isbn.jpg")
        isbn = self.extract_barcode_from_image(isbn_image)
        self.assertEqual(isbn, "9781846684302")
        ean_image = cv2.imread("./tests/example_barcode_ean.jpg")
        ean = self.extract_barcode_from_image(ean_image)
        self.assertEqual(ean, "8718699688820")
        isbn_ean_image = cv2.imread("./tests/example_barcode_isbn_ean.jpg")
        isbn_ean = self.extract_barcode_from_image(isbn_ean_image)
        self.assertEqual(isbn_ean, "9781846684302")
        missing_image = cv2.imread("./tests/example_barcode_missing.jpg")
        missing = self.extract_barcode_from_image(missing_image)
        self.assertIsNone(missing)

    def test_extract_ocr_from_image(self):
        ocr_image = cv2.imread("./tests/example_imprint.jpg")
        ocr = self.extract_ocr_from_image(ocr_image)
        self.assertEqual(len(ocr), 1127)
        self.assertTrue("This paperback edition published in 2013" in ocr)

if __name__ == '__main__':
    unittest.main()
