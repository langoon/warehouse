import unittest
from commands.langoon import Util
from cv2 import cv2

# Skriv en testklass för att testa Util

class TestUtil(Util, unittest.TestCase):

  def test_check_type(self):
        self.assertRaises(TypeError, self.check_type, "This is a string", int)

if __name__ == '__main__':
    unittest.main()
