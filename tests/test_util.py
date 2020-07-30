import unittest
from commands.langoon import Util

class TestUtil(Util, unittest.TestCase):

    def test_check_type(self):
        self.assertRaises(TypeError, self.check_type, "This is a string", int)
        try:
            self.check_type("This is a string", str)
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_check_keys(self):
        self.assertRaises(Exception, self.check_keys, dict({ "foo": 111, "bar": 222 }), "hello" )
        try:
            self.check_keys(dict({ "foo": 111, "bar": 222 }), "foo" )
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_check_unique(self):
        self.assertRaises(Exception, self.check_unique, dict({ "foo": 111, "bar": 222 }), "foo")
        try:
            self.check_unique(dict({ "foo": 111, "bar": 222 }), "baz" )
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_to_type(self):
        self.assertIsInstance(self.to_type("111"), int)
        self.assertIsInstance(self.to_type("111.111"), float)
        self.assertIsInstance(self.to_type("This is a string"), str)
        self.assertIsInstance(self.to_type([ 1, 2, 3 ]), list)
        self.assertIsInstance(self.to_type("TrUe"), bool)
        self.assertIsInstance(self.to_type("FaLSE"), bool)
        self.assertTrue(self.to_type("true"))
        self.assertFalse(self.to_type("false"))

    def test_get_shape(self):
        two, three = self.get_shape([ [ 1, 2, 3 ], [ 4, 5 ] ])
        self.assertEqual(two, 2)
        self.assertEqual(three, 3)
        four, five = self.get_shape([ [ 1, 2, 3 ], [ 4, 5 ], [ 6, 7, 8, 9, 10 ], [ 11 ] ])
        self.assertEqual(four, 4)
        self.assertEqual(five, 5)

if __name__ == '__main__':
    unittest.main()
