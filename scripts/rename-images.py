# use this script to rename all the image files before generating boxfiles.
# Language and font should not have spaces and preferable an abbreviated name should be used.

import os
dir = 'data'
images = [f for f in os.listdir(dir) if f.endswith(('.jpg', '.jpeg', '.png', '.tif', '.bmp'))]
print(f"{len(images)} number of images found")
lang = input('Enter The language without spaces\n')
font = input('Enter font without spaces\n')
part1 = f"{lang}.{font}.exp"
for i, image in enumerate(images):
    filename = f"{part1}{i}.{image[-3:]}"
    print(filename)
    os.rename(os.path.join(dir, image), os.path.join(dir, filename))