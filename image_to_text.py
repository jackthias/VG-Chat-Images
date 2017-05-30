from PIL import Image
from resizeimage import resizeimage
from copy import deepcopy
import numpy

import skimage
from skimage import io

width = 32
height = 8
pallet_size = 256
pallet_redux = 256 / pallet_size

def same_color(p1, p2):
    if not isinstance(p2, numpy.ndarray) or not isinstance(p1, numpy.ndarray):
        return False
    i = 0
    for color in p1:
        if p1[i] != p2[i]:
            return False
        i += 1
    return True

def reduce_color_pallet(img):
    for pixel_row in img:
        for pixel in pixel_row:
            reduce_color_pallet_pixel(pixel)

def reduce_color_pallet_pixel(pixel):
    i = 0
    for color in pixel:
        pixel[i] = (color // pallet_redux) * pallet_redux
        i += 1

with open('test-image.jpg', 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, [width, height])
        cover.save('temp.jpg', image.format)

reduced_image = skimage.io.imread('temp.jpg')
# reduced_image = skimage.img_as_int(reduced_image)

reduce_color_pallet(reduced_image)

skimage.io.imsave('{}-bit-temp.jpg'.format(pallet_size), reduced_image)

# print(reduced_image)
str_out = ""
prev_pixel = ""
for pixel_row in reduced_image:
    for pixel in pixel_row:
        if not same_color(pixel, prev_pixel):
            str_out = str_out + "{%s,%s,%s}🎱" % (pixel[0], pixel[1], pixel[2])
            prev_pixel = deepcopy(pixel)
        else:
            str_out = str_out + "🎱"
    str_out = str_out + "\n\n"

f_out = open('output.txt', 'w')
f_out.write(str_out)
