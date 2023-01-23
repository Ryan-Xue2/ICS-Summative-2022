import glob
import os
import numpy as np
from PIL import Image

PATH = r'src\images\kirby'
files = glob.glob(PATH + '/**/*.gif', recursive=True)
print(files)

for file_name in files:
    print(file_name)
    print(type(file_name))
    image = Image.open(file_name)
    image = image.convert("RGBA")
    arr = np.asarray(image)
    target = arr[0, 0]
    print(arr.shape)
    arr = arr.tolist()

    pixels_to_check = [(0, 0)]
    while pixels_to_check:
        to_remove = []
        for i, j in pixels_to_check:
            to_remove.append((i, j))
            if arr[i-1][j] == (255, 255, 255, 1):
                pixels_to_check.append((i-1, j))
                arr[i-1][j] == (255, 255, 255, 0)
            if arr[i+1][j] == (255, 255, 255, 1):
                pixels_to_check.append((i+1, j))
                arr[i+1][j] == (255, 255, 255, 0)
            if arr[i][j-1] == (255, 255, 255, 1):
                pixels_to_check.append((i, j-1))
                arr[i][j-1] == (255, 255, 255, 0)
            if arr[i][j+1] == (255, 255, 255, 1):
                pixels_to_check.append((i, j+1))
                arr[i][j+1] == (255, 255, 255, 0)
        for pxl in to_remove:
            pixels_to_check.remove(pxl)
    image = Image.fromarray(np.array(arr))
    image.show()
    break