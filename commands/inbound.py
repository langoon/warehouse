#!/usr/bin/env python3

import json
from cv2 import cv2
from langoon import Command, Metadata, Image, Window
from yellow import Yellow

PACKINGSLIP = [
    [
        {
            "prop": "packingslip1",
            "title": "Följesedel 1",
        },
        {
            "prop": "packingslip2",
            "title": "Följesedel 2",
        },
        {
            "prop": "packingslip3",
            "title": "Följesedel 3",
        },
        {
            "prop": "packingslip4",
            "title": "Följesedel 4",
        },
    ],
    [
        {
            "prop": "packingslip_submit",
            "title": "När alla fraktsedlar är klara – gå vidare",
            "columnspan": 4
        }
    ]
]

RECEIVE = [
    [
        {
            "prop": "backcover",
            "title": "Baksida",
        },
        {
            "prop": "receive",
            "title": "Inleverans",
            "fields": [
                {
                    "prop": "barcode",
                    "type": "text",
                    "title": "Streckkod"
                },
                {
                    "prop": "quantity",
                    "type": "text",
                    "title": "Antal"
                },
                {
                    "prop": "purchaseorder_number",
                    "type": "text",
                    "title": "Inköpsorder"
                }
            ]
        }
    ]
]

class Inbound(Command, Metadata, Image, Window):

    def __init__(self, **arguments):

        self.parse_options(**arguments)

        self.purchaseorders = json.loads(open("./tests/example_purchaseorders.json", "r").read())
        self.matched_purchaseorders = set()

        self.create_packingslip()

    def create_packingslip(self):

        self.packingslip_window = self.parse_window("Följesedlar", PACKINGSLIP)

        packingslip1_fieldset = self.get_widget("packingslip1")
        packingslip1_button = self.create_button(packingslip1_fieldset, "Ta bild", self.process_packingslip(packingslip1_fieldset))

        packingslip2_fieldset = self.get_widget("packingslip2")
        packingslip2_button = self.create_button(packingslip2_fieldset, "Ta bild", self.process_packingslip(packingslip2_fieldset))

        packingslip3_fieldset = self.get_widget("packingslip3")
        packingslip3_button = self.create_button(packingslip3_fieldset, "Ta bild", self.process_packingslip(packingslip3_fieldset))

        packingslip4_fieldset = self.get_widget("packingslip4")
        packingslip4_button = self.create_button(packingslip4_fieldset, "Ta bild", self.process_packingslip(packingslip4_fieldset))

        packingslip_submit_fieldset = self.get_widget("packingslip_submit")
        packingslip_submit_button = self.create_button(packingslip_submit_fieldset, "Gå vidare", self.submit_packingslips)

        self.packingslip_window.mainloop()

    def create_receive(self):
        self.recive_window = self.parse_window("Inleverans", RECEIVE)

        backcover_fieldset = self.get_widget("backcover")
        backcover_button = self.create_button(backcover_fieldset, "Ta bild", self.process_backcover(backcover_fieldset))

        self.recive_window.mainloop()

    def process_packingslip(self, parent):
        def callback():
            image = cv2.imread("./tests/example_packingslip.png")
            label = self.create_image(parent, image=image, width=parent.winfo_width() - 100)
            ocr = self.extract_ocr_from_image("./tests/example_packingslip.png")
            self.find_purchaseorders(ocr)
        return callback

    def process_backcover(self, parent):
        def callback():
            image = cv2.imread("./tests/example_backcover.jpg")
            # label = self.create_image(parent, image=image, height=parent.winfo_height() - 100)
            barcode = self.extract_barcode_from_image(image)
            self.set_value("receive", "barcode", barcode)
            # Check if metadata  does not exist
            if True:
                Yellow()

        return callback

    def find_purchaseorders(self, ocr):
        for purchaseorder in self.purchaseorders:
            purchaseorder_number = purchaseorder["purchaseorder_number"]
            if purchaseorder_number in ocr:
                self.matched_purchaseorders.add(purchaseorder_number)

    def submit_packingslips(self):
        self.packingslip_window.withdraw()
        self.create_receive()


if __name__ == "__main__":
    Inbound()
