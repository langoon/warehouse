#!/usr/bin/env python3

from cv2 import cv2
from langoon import Command, Metadata, Image, Window

GRID = [
    [
        {
            "prop": "frontcover",
            "title": "Framsida",
        },
        {
            "prop": "backcover",
            "title": "Baksida",
        },
        {
            "prop": "imprint",
            "title": "Försättsblad",
        }
    ],
    [
        {
            "prop": "dimensions",
            "title": "Dimensioner",
            "fields": [
                {
                    "prop": "height",
                    "type": "text",
                    "title": "Höjd",
                    "caption": "mm",
                },
                {
                    "prop": "width",
                    "type": "text",
                    "title": "Bredd",
                    "caption": "mm",
                },
                {
                    "prop": "thickness",
                    "type": "text",
                    "title": "Tjocklek",
                    "caption": "mm",
                }
            ]
        },
        {
            "prop": "properties",
            "title": "Egenskaper",
            "fields": [
                {
                    "prop": "pages",
                    "type": "text",
                    "title": "Sidor"
                },
                {
                    "prop": "weight",
                    "type": "text",
                    "title": "Vikt",
                    "caption": "g",
                },
                {
                    "prop": "sku",
                    "type": "text",
                    "title": "Hyllplats"
                },
                {
                    "prop": "barcode",
                    "type": "text",
                    "title": "Streckkod",
                } 
            ]
        }
    ]
]

class Yellow(Command, Metadata, Image, Window):

    def __init__(self, **arguments):

        self.parse_options(**arguments)

        window = self.parse_window("Gul zon", GRID, "#ffff9d")

        frontcover_fieldset = self.get_widget("frontcover")
        frontcover_button = self.create_button(frontcover_fieldset, "Ta bild", self.process_frontcover(frontcover_fieldset))

        backcover_fieldset = self.get_widget("backcover")
        backcover_button = self.create_button(backcover_fieldset, "Ta bild", self.process_backcover(backcover_fieldset))

        imprint_fieldset = self.get_widget("imprint")
        imprint_button = self.create_button(imprint_fieldset, "Ta bild", self.process_imprint(imprint_fieldset))

        window.mainloop()

        self.frontcover = None
        self.backcover = None
        self.imprint = None

    def process_image(self, parent, image_path):
        # Takes an image, optimizes it and displays it to the user

        # TODO: Should get imnage from picamera
        image = cv2.imread(image_path)

        coordinates = self.extract_section_coordinates_from_image(image, self.options["threshold_breakpoint"])
        cover = self.crop_section_from_image(image, coordinates, self.options["crop"])
        label = self.create_image(parent, image=cover, height=parent.winfo_height() - 100)

        return cover

    def process_frontcover(self, parent):
        def callback():
            self.frontcover = self.process_image(parent, "./tests/example_frontcover.jpg")
            height, width = self.extract_dimensions_from_image(self.frontcover, self.options["pixels_per_metric"])
            self.set_value("dimensions", "height", int(height))
            self.set_value("dimensions", "width", int(width))
        return callback

    def process_backcover(self, parent):
        def callback():
            self.backcover = self.process_image(parent, "./tests/example_backcover.jpg")
            barcode = self.extract_barcode_from_image(self.backcover)
            self.extract_metadata_from_barcode(barcode)
            self.set_value("properties", "barcode", barcode)
        return callback

    def process_imprint(self, parent):
        def callback():
            self.imprint = self.extract_ocr_from_image("./tests/example_imprint.jpg")
            print(self.imprint)
        return callback

    def submit(self):
        print("Submitted!")

if __name__ == "__main__":
    Yellow(threshold_breakpoint=100, crop=10, pixels_per_metric=130)
