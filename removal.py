# Assumption:
# - All picture samples have the same dimenstion
# - All picture samples are static (camera and objects in focus are stationary)

import numpy as np
import cv2 as cv

def reflectionRemoval(*pics):
    # Exit if there are not pictures
    if len(pics) == 0:
        print "No pictures assigned as sample"
        return
    
    # Initialise output as first picture
    output = np.float32(cv.imread(pics[0], cv.IMREAD_COLOR))

    # Average each picture
    for index in xrange(1, len(pics)):
        image = np.float32(cv.imread(pics[index], cv.IMREAD_COLOR))
        output = (index / (index + 1.0)) * output + (1.0 / (index + 1.0)) * image
    
    # Convert image to uint8
    output = cv.convertScaleAbs(output)

    # Show the image
    cv.imshow("averaged", output)
    cv.waitKey(0)
    cv.destroyAllWindows()

def main():
    files_lores = [
        "2m.png", "3m.png", "4m.png",
        "5m.png", "6m.png", "7m.png",
        "8m.png", "9m.png", "10m.png",
        "11m.png", "12m.png", "13m.png",
        "14m.png", "15m.png", "16m.png",
        "17m.png", "18m.png", "19m.png",
        "20m.png"
    ]
    
    files_hires = [
        "2.png", "3.png", "4.png",
        "5.png", "6.png", "7.png",
        "8.png", "9.png", "10.png",
        "11.png", "12.png", "13.png",
        "14.png", "15.png", "16.png",
        "17.png", "18.png", "19.png",
        "20.png"
    ]

    reflectionRemoval(*files_hires)

if __name__ == "__main__":
    main()