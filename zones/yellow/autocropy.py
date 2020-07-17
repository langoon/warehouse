from cv2 import cv2
import numpy as np
import sys
import os
import glob

def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect

def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([[0, 0],
                    [maxWidth - 1, 0],
                    [maxWidth - 1, maxHeight - 1],
                    [0, maxHeight - 1]], dtype = "float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
 
    # return the warped image
    return warped

def cont(img, gray, user_thresh, crop, filename):
    found = False
    cwd = os.getcwd() + '/crop/'
    orig_thresh = user_thresh
    im_h, im_w = img.shape[:2]
    while found == False: # repeat to find the right threshold value for finding a rectangle
        if user_thresh < 200:
            user_thresh = orig_thresh + 5
            orig_thresh = user_thresh
            print(user_thresh)
        ret,thresh = cv2.threshold(gray,user_thresh,255,cv2.THRESH_BINARY)
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        im_area = im_w * im_h
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > (im_area/6) and area < (im_area/1.01):
                epsilon = 0.1*cv2.arcLength(cnt,True)
                approx = cv2.approxPolyDP(cnt,epsilon,True)
                if len(approx) == 4:
                    found = True
                else:
                    user_thresh = user_thresh - 1
                    break
                rect = np.zeros((4, 2), dtype = "float32")
                rect[0] = approx[0]
                rect[1] = approx[1]
                rect[2] = approx[2]
                rect[3] = approx[3]

                dst = four_point_transform(img, rect)
                dst_h, dst_w = dst.shape[:2]
                img = dst[crop:dst_h-crop, crop:dst_w-crop]
                dst_h, dst_w = img.shape[:2]
                print("Saveing to "+cwd+"crop_"+filename)
                cv2.imwrite(cwd+"crop_"+filename, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                #res = cv2.resize(img,(dst_w/6, dst_h/6), interpolation = cv2.INTER_CUBIC)

    return found, im_w, im_h

def main(thresh, crop, filename):
    img = cv2.imread(filename)
    print("Opening: "+filename)

    #add white background (in case one side is cropped right already, otherwise script would fail finding contours)
    img = cv2.copyMakeBorder(img,100,100,100,100, cv2.BORDER_CONSTANT,value=[255,255,255])
    im_h, im_w = img.shape[:2]
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    res_gray = cv2.resize(img,(int(im_w/6), int(im_h/6)), interpolation = cv2.INTER_CUBIC)
    found, im_w, im_h = cont(img, gray, thresh, crop, filename)


os.system("mkdir crop") #create folder for cropped images

if len(sys.argv) < 2:
    thresh = 220 #standard starting threshold value (used to be a good compromise) -> can easily be smaller for pictures without white border
    crop = 15 #standard extra crop -> pixel cropped after automatic crop/rotate (otherwise often unclean borders)
elif len(sys.argv) < 3:
    thresh = int(sys.argv[1])
    crop = 15
elif len(sys.argv) < 4:
    thresh = int(sys.argv[1])
    crop = int(sys.argv[2])
elif len(sys.argv) >= 4:
    print("USAGE: python img_extract_contour.py TRESHOLD MIN_CROP")

files = []
types = ('*.bmp','*.BMP','*.tiff','*.TIFF','*.tif','*.TIF','*.jpg', '*.JPG','*.JPEG', '*.jpeg', '*.png', '*.PNG') #all should work but only .jpg was tested
for t in types:
    if glob.glob(t) != []:
        files.append(glob.glob(t))
for f in files[0]:
    main(thresh, crop, f)
