from sklearn.metrics import mean_squared_error as mse
import argparse
import logging
import os
import time
import numpy as np
import utils as U
import cv2 as cv
from PIL import Image
from pcp import pcp

import reader

logger = logging.getLogger(__name__)

###############################################################################################################################
## Parse arguments
#

parser = argparse.ArgumentParser()
parser.add_argument("-path", "--image-path", dest="image_path", type=str, metavar='<str>', default=None, help="The path to the folder containing the images")
parser.add_argument("-a", "--algorithm", dest="algorithm", type=str, metavar='<str>', default="averaging", help="Algorithm to do reflection removal (averaging|rpca) (default=averaging)")
parser.add_argument("-i", "--iter", dest="num_iter", type=int, metavar='<int>', default=50, help="Number of iteration for rpca (default=50)")
parser.add_argument("-m", "--method", dest="rpca_method", type=str, metavar='<str>', default="exact", help="RPCA method (approximate|exact|sparse)")
parser.add_argument("-ref", "--ref-image-name", dest="ref_image_name", type=str, metavar='<str>', default=None, help="Name to the ref image (i.e., Original image without reflection)")
parser.add_argument("-o", "--out-dir", dest="out_dir_path", type=str, metavar='<str>', required=True, help="The path to the output directory")
parser.add_argument("-show", "--show-image", dest="is_show_image_popup", action='store_true', help="Set this flag to make the averaged image shown in a popup window")

args = parser.parse_args()

image_path = args.image_path
algorithm = args.algorithm
num_iter = args.num_iter
rpca_method = args.rpca_method
ref_image_name = args.ref_image_name
out_dir = args.out_dir_path
is_show_image_popup = args.is_show_image_popup

assert rpca_method in {"exact", "approximate", "sparse"}
assert algorithm in {"averaging", "rpca"}

U.mkdir_p(out_dir)
U.set_logger(out_dir)
U.print_args(args)

# Assumption:
# - All picture samples have the same dimenstion
# - All picture samples are static (camera and objects in focus are stationary)


def doAveraging(image_filenames, ref_file):
    st = U.Stopwatch()
    st.start()
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
    
    logger.info("Finished in " + str(st.stop()))
    ref = cv.imread(ref_file, cv.IMREAD_COLOR)
    logger.info("With mse " + str(mse(ref.flatten(), averagedImage.flatten())))

    # save image
    averagedImagePath = out_dir + '/averaged_image.jpg'
    cv.imwrite(averagedImagePath, averagedImage)

    # Show the image
    if is_show_image_popup:
        cv.imshow("averaged", averagedImage)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
    logger.info("Averaging completed!")
    logger.info("Image saved in %s", averagedImagePath)
    
def process_image(filenames):
    matrix = []
    shape = None
    for image_file in filenames:
        img = Image.open(image_file).convert("RGB")
        if shape is None:
            shape = img.size
        assert img.size == shape
        imgArr = np.array(img.getdata())
        matrix.append(imgArr)
    return np.array(matrix), shape[::-1]

def doRpca(image_filenames, ref_file):
    start = time.time()
    M, dimension = process_image(image_filenames)
    
    # shape[0] is the number of images in the dataset
    # shape[1] is the pixel values for either r,g or b (width x height, flattened)
    # shape[2] is 3, because it consists of r,g,b
    M = np.reshape(M,(M.shape[0],M.shape[1]*M.shape[2]))
    
    logger.info(M.shape)
    logger.info(dimension)
    L, S, (u, s, v) = pcp(M, maxiter=num_iter, verbose=True, svd_method=rpca_method)
    M = np.reshape(M,(M.shape[0],int(M.shape[1]/3),3))
    L = np.reshape(L,(L.shape[0],int(L.shape[1]/3),3))
    S = np.reshape(S,(S.shape[0],int(S.shape[1]/3),3))

    ref = cv.imread(ref_file, cv.IMREAD_COLOR)

    for i in range (len(M)):
        base = os.path.basename(image_filenames[i])
        ext = os.path.splitext(base)[1]
        current_filename = os.path.splitext(base)[0]
        
        testM = np.reshape(M[i],(dimension[0],dimension[1],3))
        testM = np.uint8(testM)
        imgM = Image.fromarray(testM)
        imgM.save(out_dir+"/"+current_filename+"-ori.png")
        
        testL = np.reshape(L[i],(dimension[0],dimension[1],3))
        testL = np.uint8(testL)
        imgL = Image.fromarray(testL)
        imgL.save(out_dir+"/"+current_filename+"-lowrank.png")
        
        testS = np.reshape(S[i],(dimension[0],dimension[1],3))
        testS = np.uint8(testS)
        imgS = Image.fromarray(testS)
        imgS.save(out_dir+"/"+current_filename+"-sparse.png")

        # logger.info(current_filename + ext + " Original MSE : " + str(mse(ref.flatten(), M[i].flatten())))
        logger.info(current_filename + ext + " Low-rank MSE : " + str(mse(ref.flatten(), L[i].flatten())))
        
    logger.info("RPCA completed!")
    rpca_time = time.time() - start
    logger.info("RPCA total time taken = %.3f seconds" % rpca_time)

####################################################################
# Main functions here
####################################################################

if (__name__ == "__main__"):
    image_filenames, ref_file = reader.getImagePaths(image_path, ref_image_name)
    if algorithm == 'averaging':
        doAveraging(image_filenames, ref_file)
    elif algorithm == 'rpca':
        doRpca(image_filenames, ref_file)
    else:
        logger.error("Invalid algorithm choice!")
