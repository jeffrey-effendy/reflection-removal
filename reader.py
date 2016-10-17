import glob
import logging
logger = logging.getLogger(__name__)

def getImagePaths(dir_path, ref_filename):
    image_filenames = []
    image_dir_path = glob.glob(dir_path + "/*")
    for file_path in image_dir_path:
        if ref_filename not in file_path:
            image_filenames.append(file_path)
    logger.info(" %i images have been successfully read!", len(image_filenames))
    return image_filenames
    