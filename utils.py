
import numpy as np
import pandas as pd
from PIL import Image


def imgToArray(path,size = None, norm=True):
    print(12)
    im = Image.open(path)
    ar = np.asarray(im)
    if size:
        im = im.resize((size,size))
    if norm:
        ar = (ar-127.5)/127.5
    return ar




def arrayToIm(array,size = None):
    array = (array*127.5) + 127.5
    im = Image.fromarray(array)
    if size:
        im.resize((size,size))
    im.show()
    return im

a = imgToArray('./test_photo.png')
print(a)    