#!/usr/bin/env python

import os
import fnmatch
from shutil import copyfile
from localsettings import MUSIC_LOCATION

covers_dir = "{}/covers/".format(os.path.dirname(os.path.realpath(__file__)))

images = []

# find all the images
for root, dirnames, filenames in os.walk(covers_dir):
    for filename in fnmatch.filter(filenames, '*.png'):
        images.append(os.path.join(root, filename))

# copy those fuckers
for image in images:
    print 'copying {}'.format(image)

    destination = image.replace(covers_dir, '')
    destination = '{}/{}'.format(MUSIC_LOCATION, destination)
    copyfile(image, destination)

print ''
print 'Done!'
print ''
