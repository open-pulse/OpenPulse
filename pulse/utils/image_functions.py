from PIL import Image
import numpy as np
from scipy.ndimage import binary_dilation


def removes_image_background(image: Image):
    image = image.convert("RGBA")
    np_image = np.array(image)
    # calculate difference between pixel color and pink background color
    diff = np_image[:,:,:3] - np.array((247, 0, 255))
    # calculate norm of difference
    norm = np.linalg.norm(diff, axis=2)
    # create mask where norm is less than 20
    mask = norm < 20
    # apply dilation to the mask to remove any remaining lines near the edge
    mask = binary_dilation(mask, iterations=1)
    # set alpha channel to 0 where mask is True
    np_image[:,:,3][mask] = 0

    return Image.fromarray(np_image)
