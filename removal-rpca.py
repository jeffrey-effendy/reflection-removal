import argparse
import logging
import numpy as np
import utils as U
import cv2 as cv
import os
import reader

logger = logging.getLogger(__name__)

###############################################################################################################################
## Parse arguments
#

parser = argparse.ArgumentParser()
parser.add_argument("-path", "--image-path", dest="image_path", type=str, metavar='<str>', default=None, help="The path to the folder containing the images")
parser.add_argument("-ref", "--ref-image-name", dest="ref_image_name", type=str, metavar='<str>', default=None, help="Name to the ref image (i.e., Original image without reflection)")
parser.add_argument("-o", "--out-dir", dest="out_dir_path", type=str, metavar='<str>', default=os.getcwd(), help="The path to the output directory")
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

def softThreshold(M, eps):
    for i, j in [(i, j) for i in xrange(M.shape[0]) for j in xrange(M.shape[1])]:
        if M[i,j] > eps:
            M[i,j] = M[i,j] - eps
        elif M[i,j] < -1 * eps:
            M[i,j] = M[i,j] + eps
        else:
            M[i,j] = 0
    return M

def rpca(image_filenames):
    logger.info("Starting to process images, and perform averaging...")
    
    # Exit if there are not pictures
    if len(image_filenames) == 0:
        logger.error("Error, no images are included! in function doReflectionRemoval()")
        return
    
    # Matrix D will be the vertically stacked flatten image matrices
    D = np.float32(cv.imread(image_filenames[0], cv.IMREAD_COLOR)).flatten()
    for i in xrange(1, len(image_filenames)):
        image = np.float32(cv.imread(image_filenames[i], cv.IMREAD_COLOR)).flatten()
        D = np.vstack((D, image))
    
    # Initialise background as B and reflection as R
    B = np.zeros(D.shape, dtype=np.float32)
    R = np.zeros(D.shape, dtype=np.float32)

    # Initialise lagrange constants L and penalty constants mu and rho
    L = np.ones(D.shape, dtype=np.float32)
    mu = 1.0
    rho = 2.0

    U,S,V = np.linalg.svd(D - R + (1 / mu) * L)
    B = U.dot(softThreshold(S, 1 / mu)).dot(V.T)
    R = softThreshold(D - B + (1 / mu) * L)

    print B
    print R


####################################################################
# Main functions here
####################################################################

if (__name__ == "__main__"):
    image_filenames = reader.getImagePaths(image_path, ref_image_name)
    rpca(image_filenames)
