#!/usr/bin/env python

from PIL import Image
import os
import fnmatch


root = '/Volumes/Lossless/Lossless'
images = []


print 'xxxxxxxxxxxxx'
print 'x hey there x'
print 'xxxxxxxxxxxxx'
print ''
print 'Finding images...'


os.chdir(root)

for root, dirnames, filenames in os.walk(root):
    for filename in filenames:
        is_png = '.png' in filename
        is_jpg = '.jpg' in filename
        is_jpeg = '.jpeg' in filename

        if is_png or is_jpg or is_jpeg:
            images.append(os.path.join(root, filename))


print '{} images found'.format(len(images))
print ''


def check_filename(path):
    return {
        'success': True,
    }
