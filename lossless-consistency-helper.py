#!/usr/bin/env python

from PIL import Image
import os
import fnmatch


# helpers
# ------------------------------------------------------------------------------

def add_error_to_res(path, error):
    if not res.get(path):
        res[path] = []

    res[path].append(error)


def check_filename(path):
    is_good_png = 'cover.png' in path
    is_good_jpg = 'cover.jpg' in path
    is_good_jpeg = 'cover.jpeg' in path

    if is_good_png or is_good_jpg or is_good_jpeg:
        return {
            'success': True,
        }
    else:
        return {
            'success': False,
            'error': 'Bad filename'
        }


# script
# ------------------------------------------------------------------------------

root = '/Volumes/Lossless/Lossless'
images = []
res = {}

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


print 'Looking for images named something other than "cover"...'

for image in images:
    filename_check = check_filename(image)

    if not filename_check['success']:
        add_error_to_res(image, filename_check['error'])

print res
