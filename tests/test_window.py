import unittest
from cv2 import cv2
from tkinter import Entry, Button, Label, LabelFrame, Frame, Tk
from commands.langoon import Window

class TestWindow(Window, unittest.TestCase):

    def setUp(self):
        self.window = {
            "values": {},
            "widgets": {}
        }
        self.parent = Frame()

    def tearDown(self):
        self.parent.destroy()

    def test_parse_window(self):
        self.assertRaises(TypeError, self.parse_window, "this is a title", "wrong shape")
        self.assertRaises(TypeError, self.parse_window, "this is a title", [ "wrong shape" ])
        self.assertRaises(TypeError, self.parse_window, "this is a title", [ [ "wrong shape" ] ])
        self.assertRaises(Exception, self.parse_window, "this is a title", [ [ { "missing_prop": 111 } ] ])
        self.assertRaises(Exception, self.parse_window, "this is a title", [ [ { "prop": "not_unique", "fields": { "prop": "any", "type": "text", "title": "text" } }, { "prop": "not_unique", "fields": { "prop": "any", "type": "text", "title": "text" } } ] ])
        self.assertRaises(Exception, self.parse_window, "this is a title", [ [ { "prop": "first", "columnspan": 3, "rowspan": 2 }], [ { "prop": "second" }, { "prop": "third" } ] ],)
        self.assertRaises(Exception, self.parse_window, "this is a title", [ [ { "prop": "first", "columnspan": 2, "rowspan": 3 }], [ { "prop": "second" }, { "prop": "third" } ] ])
        self.assertRaises(Exception, self.parse_window, "this is a title", [ [ { "prop": "first", "columnspan": 2 }, { "prop": "second", "offset": 1 } ] ])
        parent = self.parse_window("this is a title", [ [ { "prop": "any" } ] ])
        self.assertIsInstance(parent, Tk)
        parent.destroy()

    def test_parse_fields(self):
        self.assertRaises(TypeError, self.parse_fields, self.parent, "frame_prop", "wrong type")
        self.assertRaises(TypeError, self.parse_fields, self.parent, "frame_prop", [ "wrong type" ])
        self.assertRaises(Exception, self.parse_fields, self.parent, "frame_prop", [ { "missing_prop": 111 } ])
        self.assertRaises(Exception, self.parse_fields, self.parent, "frame_prop", [ { "prop": "not_unique", "title": "any", "type": "text" }, { "prop": "not_unique", "title": "any", "type": "text" } ])
        self.assertRaises(Exception, self.parse_fields, self.parent, "frame_prop", [ { "prop": "any", "title": "any", "type": "wrong_type" } ])
        self.window = {
            "values": {},
            "widgets": {}
        }
        self.parse_fields(self.parent, "frame_prop", [ { "prop": "field_prop", "title": "any", "type": "text", "value": 111 } ])
        self.assertDictEqual(self.window["values"], { "frame_prop": { "field_prop": 111 } })

    def test_create_window(self):
        self.assertIsInstance(self.create_window("this is a title"), Tk)

    def test_create_frame(self):
        self.assertIsInstance(self.create_frame(self.parent, "this is a frame"), LabelFrame)
        self.assertIsInstance(self.create_frame(self.parent), Frame)

    def test_create_text(self):
        self.assertIsInstance(self.create_text(self.parent, "this is a title"), Entry)

    def test_create_button(self):
        def callback():
            pass
        self.assertIsInstance(self.create_button(self.parent, "this is a title", callback), Button)

    def test_create_image(self):
        image_path = self.create_image(self.parent, "./tests/example_imprint.jpg")
        image_resized_width = self.create_image(self.parent, "./tests/example_imprint.jpg", width=100)
        image_resized_width.update()
        image_resized_height = self.create_image(self.parent, "./tests/example_imprint.jpg", height=100)
        image_resized_height.update()
        image_cv2 = self.create_image(self.parent, cv2.imread("./tests/example_imprint.jpg"))
        self.assertIsInstance(image_path, Label)
        self.assertIsInstance(image_cv2, Label)
        self.assertEqual(str(image_path.cget("width")), "3024")
        self.assertEqual(str(image_path.cget("height")), "4032")
        self.assertEqual(str(image_resized_width.cget("width")), "100")
        self.assertEqual(str(image_resized_width.cget("height")), "133")
        self.assertEqual(str(image_resized_height.cget("height")), "100")
        self.assertEqual(str(image_resized_height.cget("width")), "75")

    def test_set_widget(self):
        self.set_widget(111, "frame_prop")
        self.assertDictEqual(self.window, { "widgets": { "frame_prop": 111 }, "values": {} })
        self.set_widget(222, "frame_prop", "field_prop")
        self.assertDictEqual(self.window, { "widgets": {  "frame_prop": 111, "frame_prop.field_prop": 222 }, "values": {} })

    def test_get_widget(self):
        self.window = { "widgets": { "frame_prop": 111, "frame_prop.field_prop": 222 } }
        self.assertEqual(111, self.get_widget("frame_prop"))
        self.assertEqual(222, self.get_widget("frame_prop", "field_prop"))

    def test_set_value(self):
        self.window = { "widgets": { "frame_prop.field_prop": Entry() }, "values": {} }
        self.set_value("frame_prop", "field_prop", 1111)
        self.assertEqual(self.window["values"]["frame_prop"]["field_prop"], 1111)
        self.assertEqual(self.window["widgets"]["frame_prop.field_prop"].get(), "1111")

    def test_get_value(self):
        self.window = { "values": { "frame_prop": { "field_prop": 111 } } }
        self.assertEqual(111, self.get_value("frame_prop", "field_prop"))

if __name__ == '__main__':
    unittest.main()
