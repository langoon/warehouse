# A shared Langoon library of utility functions used for extracting an processing book metadata

import sys
import inspect
import json
import numpy
import PIL.Image
import PIL.ImageTk
import tkinter
import isbnlib
import pytesseract
from pyzbar.pyzbar import decode
# import picamera
from cv2 import cv2

class Util:
    # Utilities used for all classes

    def check_type(self, check, check_type):
        # Check if the provided check object is of the specified type
        if not isinstance(check, check_type):
            raise TypeError("The object is not a " + check_type.__name__, check)

    def check_keys(self, check, *keys):
        # Check if provided dictionary has all the required keys
        for key in keys:
            if not key in check:
                raise Exception("The dictionary is missing required key " + key, check)

    def check_unique(self, check, key):
        # Check that the check dictionary does not have the provided key
        if key in check:
            raise Exception("The key " + key + " already exist on this dictionary", check)

    def to_type(self, value):
        # Parse unknown value into int, float or bool

        if isinstance(value, str):

            # To int
            try:
                return int(value)
            except ValueError:
                pass

            # To float
            try:
                return float(value)
            except ValueError:
                pass

            # To bool
            if value.lower() == 'true':
                return bool(True)
            if value.lower() == 'false':
                return bool(False)

            # To str
            return value

        else:
            return value

    def get_shape(self, array):
        # Returns the maximum shape of a jagged multi-dimensional array

        return len(array), max(map(lambda x: len(x), array))

class Window(Util):
    # Utilities used for creating GUI interfaces

    def parse_window(self, title, grid, color=None):
        # Takes a multi-dimensional list model and generates it into a GUI grid

        # Size of the grid container width as a percentage of the window's total screen area
        CONTAINER_WIDTH = .6
        # Aspect ratio between the grid's width to height
        RATIO = .75
        # Margin between the frames in the grid
        MARGIN = 10

        # Create a class attribute dictionary to store the widgets and its values
        self.window = {
            "widgets": {},
            "values": {}
        }

        window = self.create_window(title, color)

        container_widget = tkinter.Frame(window)

        container_widget.place(
            relwidth = CONTAINER_WIDTH,
            relheight = CONTAINER_WIDTH / RATIO,
            relx = (1 - CONTAINER_WIDTH) / 2,
            rely = (1 - CONTAINER_WIDTH / RATIO) / 2
        )

        # Get the shape of the grid
        rows, columns = self.get_shape(grid)

        # Draw the dimensions of the grid
        container_widget.rowconfigure(rows - 1, weight=1)
        container_widget.columnconfigure(columns - 1, weight=1)

        self.check_type(grid, list)
        for row_index, row in enumerate(grid):
            self.check_type(row, list)
            for column_index, column in enumerate(row):
                self.check_type(column, dict)
                self.check_keys(column, "prop")
                self.check_unique(self.window["values"], column.get("prop"))
                
                frame_prop = column.get("prop")
                title = column.get("title")
                border = column.get("border")
                fields = column.get("fields")
                columnspan = column.get("columnspan")
                rowspan = column.get("rowspan")
                offset = column.get("offset")

                if columnspan is None:
                    columnspan = 1

                if rowspan is None:
                    rowspan = 1

                if offset is None:
                    offset = 0
 
                if column_index + (columnspan - 1) + offset > columns:
                    raise Exception("The columns are exceeding the size of the grid. Check your columnspan/rowspan settings.")

                if row_index + (rowspan - 1) > rows:
                    raise Exception("The rows are exceeding the size of the grid. Check your columnspan/rowspan settings.")

                # Update container in order to get it's dimensions
                container_widget.update()

                height = (container_widget.winfo_height() / rows) * rowspan
                width = (container_widget.winfo_width() / columns) * columnspan

                wrapper_widget = tkinter.Frame(
                    container_widget,
                    padx=MARGIN,
                    pady=MARGIN,
                    width=width,
                    height=height
                )

                wrapper_widget.grid(
                    row=row_index,
                    column=column_index + offset,
                    rowspan=rowspan,
                    columnspan=columnspan,
                    sticky=tkinter.NSEW
                )

                wrapper_widget.propagate(False)

                frame_widget = self.create_frame(wrapper_widget, title)

                self.set_widget(frame_widget, frame_prop)

                if fields:
                    self.parse_fields(frame_widget, frame_prop, fields)

        return window

    def parse_fields(self, frame, frame_prop, fields):
        # Takes a single dimensional list of dictionaries representing input fields and generates it into GUI widgets

        for field in fields:
            self.check_type(field, dict)
            self.check_keys(field, "prop", "title", "type")

            field_prop = field.get("prop")

            if frame_prop not in self.window["values"]:
                self.window["values"][frame_prop] = {}

            self.check_unique(self.window["values"][frame_prop], field_prop)

            title = field.get("title")
            field_type = field.get("type")
            value = field.get("value")

            if field_type not in ("text", "radio", "checkbox"):
                raise Exception("The type " + field_type + " must be text, radio, checkbox")

            if field_type == "text":
                caption = field.get("caption")
                field_widget = self.create_text(frame, title, caption)

            self.set_widget(field_widget, frame_prop, field_prop)
            self.set_value(frame_prop, field_prop, value)

    def create_window(self, title, color=None):
        # Creates and returns the window object
        window = tkinter.Tk()
        window.title(title)
        window.attributes("-fullscreen", True)

        if color:
            window.configure(background=color)

        return window

    def create_frame(self, parent, title=None, border=2):
        # Creates and returns a Frame or LabelFrame

        # Padding for the frames
        PADDING = 20

        # Default frame options
        OPTIONS = {
            "padx": PADDING,
            "pady": PADDING,
            "borderwidth": border,
            "relief": tkinter.RIDGE 
        }

        # Return a LabelFrame if title has been provided, otherwise a regular frame
        if title is None:
            frame = tkinter.Frame(parent, **OPTIONS)
        else:
            frame = tkinter.LabelFrame(parent, text=" " + title + " ", font=("Trebuchet MS", 18), **OPTIONS)
        
        # Place frame according to provided arguments
        frame.pack(fill=tkinter.BOTH, expand=True)

        return frame

    def create_text(self, parent, title, caption=None):
        # Creates a text entry widget and returns it

        # Create the label that will be display above the entry field
        label = tkinter.Label(parent, text=title, pady=5, font=("Trebuchet MS", 16), anchor=tkinter.W)
        label.pack(fill=tkinter.X)

        # Create the frame that wraps the entry field and caption
        wrapper = tkinter.Frame(parent, borderwidth=2, relief=tkinter.SUNKEN)
        wrapper.pack(fill=tkinter.X)

        # Create the entry input field
        entry = tkinter.Entry(wrapper, borderwidth=2, relief=tkinter.FLAT, font=("Trebuchet MS", 18))

        # Create a caption that will be displayed to the right of the entry field
        if caption:
            entry.pack(expand=True, fill=tkinter.X, side=tkinter.LEFT)
            caption = tkinter.Label(wrapper, text=caption, font=("Trebuchet MS", 16), anchor=tkinter.CENTER, width=10, bg="#efefef")
            caption.pack(fill=tkinter.BOTH, side=tkinter.RIGHT)
        else:
            entry.pack(fill=tkinter.X)

        return entry


    def create_button(self, parent, title, callback):
        # Creates a button widget and returns it

        button = tkinter.Button(
            parent,
            text=title,
            command=callback
        )
        button.pack()

        return button

    def create_image(self, parent, image, width=None, height=None):
        # Creates an image label and returns it.
        # The `image` parameter may be a path or an CV2 image type.

        if isinstance(image, str):
            load = PIL.Image.open(image)
        else:
            load = PIL.Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Resize the image propotionally
        image_width, image_height = load.size
        if width is None and height is not None:
            width = int(image_width / image_height * height)
        if height is None and width is not None:
            height = int(image_width / image_height * width)
        load = load.resize((width, height))

        # Create render which can be read by Tkinter
        render = PIL.ImageTk.PhotoImage(load)
        label = tkinter.Label(parent, image=render, height=height, width=width)

        # Reattach the image to prevent garbage collection from deleting it
        label.image = render
        label.pack()

        # Push into the event stack in order for the image to be rendered
        parent.update()

        return label

    def get_widget(self, frame_prop, field_prop=None):
        # Gets a widget from `window.widgets`

        if field_prop:
            return self.window["widgets"][frame_prop + "." + field_prop]
        else:
            return self.window["widgets"][frame_prop]

    def set_widget(self, widget, frame_prop, field_prop=None):
        # Sets the widget in `window.widgets`

        if field_prop:
            self.window["widgets"][frame_prop + "." + field_prop] = widget
        else:
            self.window["widgets"][frame_prop] = widget
            
    def get_value(self, frame_prop, field_prop):
        # Gets a value from `window.values`

        if field_prop:
            return self.window["widgets"][frame_prop][field_prop]
        else:
            return self.window["widgets"][frame_prop]

    def set_value(self, frame_prop, field_prop, value):
        # Set a value in `window.values` and its respective widget

        field_widget = self.get_widget(frame_prop, field_prop)

        if value is None:
            value = ""

        field_widget.delete(0, tkinter.END)
        field_widget.insert(0, str(value))

        if not frame_prop in self.window["values"]:
            self.window["values"][frame_prop] = {}

        self.window["values"][frame_prop][field_prop] = value

class Command(Util):
    # Utilities for responding to commands

    def parse_options(self, **arguments):
        # Matches the provided arguments with the system arguments
        # If there's no match, then use the default value

        self.options = {}
          
        # Create the dictionary and set the defaults
        for key, value in arguments.items():
            self.options[key] = value

        # Apply the system arguments if applicable
        for system_argument in sys.argv[1:]:
            # System arguments are prefixed with a dash, make sure that is removed
            (key, value) = system_argument.lstrip('-').split(',')
            self.options[key] = self.to_type(value)

        # If help option parameter has been passed then respond with a help message 
        if "help" in self.options:
            print("The following options are available for this command:")
            for key in arguments:
                print(" -" + key)
            print(" -help")
            sys.exit()

        return self.options

    def send_response(self, data):
        # Parse dictionary or array into a JSON string and print it
        response = {}
        command = inspect.stack()[len(inspect.stack()) - 2][3]
        response["command"] = command
        response["options"] = self.options
        response["data"] = data
        print(json.dumps(response))

class Image:
    # Utilities used for extracting data from images

    def order_coordinates(self, coordinates):
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

    def extract_dimensions_from_image(self, image, pixels_per_metric):
        # Takes an image and calculate its width and height based on a metric
        # The metric represents the number of pixels a mm, cm, inch, etc. takes up in the image

        # Get image dimensions
        image_height, image_width = image.shape[:2]

        # Convert px dimensions into the metric value and return the height and width in that value
        return image_height / (image_width / pixels_per_metric), image_width / (image_width / pixels_per_metric)

    def crop_section_from_image(self, image, coordinates, crop):
        # Takes the coordinates for a rectangular polygon's location on an image,
        # orders those coordinates into a stright rectangle, and warps the image to fit those coordinates,
        # crops that section and returns it back

        source_rectangle = self.order_coordinates(coordinates)
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
            [0, 0],
            # Top-right
            [max_width - 1, 0],
            # Bottom-right
            [max_width - 1, max_height - 1],
            # Bottom-left
            [0, max_height - 1]
        ], dtype="float32")

        # Compute the perspective transform matrix
        matrix = cv2.getPerspectiveTransform(source_rectangle, target_rectangle)
        # Apply that transform matrix to the image
        image = cv2.warpPerspective(image, matrix, (max_width, max_height))
        # Crop the edges of the image and return it
        return image[crop: -crop, crop: -crop]

    def extract_section_coordinates_from_image(self, image, threshold_breakpoint):
        # Takes an raw image with a white bright background and looks for the contour of
        # a rectangular object and returns the coordinates representing a polygon shape of that object.
        # A threshold needs to be provided representing an acceptable breaking point at which the coordinates will be returned

        # The width of the border to wrap the image in case the object overflows the image
        BORDER_WIDTH = 100

        image = cv2.copyMakeBorder(image, BORDER_WIDTH, BORDER_WIDTH, BORDER_WIDTH,
                                BORDER_WIDTH, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Calculate the image area
        image_height, image_width = image.shape[:2]
        image_area = image_height * image_width
        # Repeat to find the right threshold value for finding a rectangle
        found = False
        # Increment the threshold until a contour is found
        threshold_current = threshold_breakpoint
        while found is False:
            if threshold_breakpoint < 200:
                threshold_breakpoint = threshold_current + 5
                threshold_current = threshold_breakpoint
            # Extract contours using threshold
            _, threshold = cv2.threshold(
                image_grayscale, threshold_breakpoint, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(
                threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
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

    def extract_barcode_from_image(self, image):
        # Takes an image finds all barcodes and returns its data and type

        decoded_barcodes = decode(image)
        GTIN13 = None

        for decoded_barcode in decoded_barcodes:
            if not isinstance(decoded_barcode, str):
                barcode = decoded_barcode.data.decode("utf-8") 
            # If ISBN 13 return it
            if isbnlib.is_isbn13(barcode):
                return barcode
            # If ISBN 10 convert to ISBN 13 and return
            if isbnlib.is_isbn10(barcode): 
                return isbnlib.to_isbn13(barcode)
            # If GTIN13, return only if no ISBN number was found
            if len(barcode) == 13:
                GTIN13 = barcode

        return GTIN13

    def extract_ocr_from_image(self, image):
        return pytesseract.image_to_string(image)

class Metadata:
    # Utilities for extracting metadata from a publication 

    def extract_metadata_from_barcode(self, barcode):
        # Takes a barcode and fetch basic metadata about this title

        try:
            goob = isbnlib.meta(barcode, service="goob")
        except:
            goob = {}

        try:
            wiki = isbnlib.meta(barcode, service="wiki")
        except:
            wiki = {}

        try:
            openl = isbnlib.meta(barcode, service="openl")
        except:
            openl = {}

        info = isbnlib.info(barcode)

        print("goob", goob)
        print("wiki", wiki)
        print("openl", openl)
        print("info", info)


        # if "Title" in metadata:
        #     title = metadata["Title"]
        # else:
        #     title = None
        # if "Publisher" in metadata:
        #     publisher = metadata["Publisher"]
        # else:
        #     publisher = None
        # if "Year" in metadata:
        #     year = metadata["Year"]
        # else:
        #     year = None
        # if "Authors" in metadata:
        #     authors = metadata["Authors"]
        # else:
        #     authors = None

        # return (
        #     title,
        #     publisher,
        #     year,
        #     authors
        # )

# TODO(unitario): picamera requires rasbian. Have not been able to make it work on my macOS environment. Chack if anything can be done.
# def capture_camera_image():
    # Captures an image with the camera and returns that as an image like object
    # There's a lot of configurations, please read about them here: https://picamera.readthedocs.io/en/release-1.13/api_camera.html#picamera
    # with picamera.PiCamera() as camera:
        # try:
            #image = io.BytesIO()
            # return camera.capture(image)
        # finally:
            # camera.close()
