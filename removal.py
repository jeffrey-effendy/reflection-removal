import argparse
import logging
import numpy as np
import utils as U
import cv2 as cv

import reader

logger = logging.getLogger(__name__)

###############################################################################################################################
## Parse arguments
#

parser = argparse.ArgumentParser()
parser.add_argument("-path", "--image-path", dest="image_path", type=str, metavar='<str>', default=None, help="The path to the folder containing the images")
parser.add_argument("-ref", "--ref-image-name", dest="ref_image_name", type=str, metavar='<str>', default=None, help="Name to the ref image (i.e., Original image without reflection)")
parser.add_argument("-o", "--out-dir", dest="out_dir_path", type=str, metavar='<str>', required=True, help="The path to the output directory")
parser.add_argument("-show", "--show-image", dest="is_show_image_popup", action='store_true', help="Set this flag to make the averaged image shown in a popup window")

args = parser.parse_args()

image_path = args.image_path
ref_image_name = args.ref_image_name
out_dir = args.out_dir_path
is_show_image_popup = args.is_show_image_popup

U.mkdir_p(out_dir)
U.set_logger(out_dir)
U.print_args(args)

# Assumption:
# - All picture samples have the same dimenstion
# - All picture samples are static (camera and objects in focus are stationary)

def doAveraging(image_filenames):
    logger.info("Starting to process images, and perform averaging...")
    # Exit if there are not pictures
    if len(image_filenames) == 0:
        logger.error("Error, no images are included! in function doReflectionRemoval()")
        return
    
    # Initialise output as first picture
    output = np.float32(cv.imread(image_filenames[0], cv.IMREAD_COLOR))

    # Average each picture
    for index in xrange(1, len(image_filenames)):
        image = np.float32(cv.imread(image_filenames[index], cv.IMREAD_COLOR))
        output = (index / (index + 1.0)) * output + (1.0 / (index + 1.0)) * image
    
    # Convert image to uint8
    averagedImage = cv.convertScaleAbs(output)
    
    # save image
    averagedImagePath = out_dir + '/averaged_image.jpg'
    cv.imwrite(averagedImagePath, averagedImage)

    # Show the image
    if is_show_image_popup:
        cv.imshow("averaged", output)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
    logger.info("Averaging completed!")
    logger.info("Image saved in %s", averagedImagePath)


####################################################################
# Main functions here
####################################################################

image_filenames = reader.getImagePaths(image_path, ref_image_name)
doAveraging(image_filenames)
