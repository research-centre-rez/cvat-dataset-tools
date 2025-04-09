import numpy as np
import numpy.typing as npt

Image = npt.NDArray[np.uint8]

def threshold_image(img: Image,thr:float)-> Image:
    if thr < 0 or thr > 255:
        raise ValueError("Threshold must be between 0 and 255")

    return np.uint8(np.where(img > 127, 255, 0))

def invert_image(img: Image) -> Image:
    return np.uint8(255 - img)
    
