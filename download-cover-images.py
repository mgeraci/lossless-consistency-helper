#!/usr/bin/env python

import os
import sys
import json
from localsettings import MUSIC_LOCATION

output_dir = os.path.dirname(os.path.realpath(__file__))
cover_dir = '{}/covers/'.format(output_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


import_file = '{}/{}'.format(output_dir, 'get-new-images-output.txt')

print 'reading {} for data...'.format(import_file)

try:
    data = open(import_file)
except:
    print 'Your passed data file was not found.'
    sys.exit()

try:
    data = json.load(data)
except:
    print 'Your passed data file was corrupt.'
    sys.exit()


print ''
print 'Hi. Hello. Greetings. Let\'s download some images!'
print '-------------------------------------------------'
print ''

for image in data:
    image_info = data[image]

    if not image_info['success']:
        continue

    if not len(image_info['result']):
        continue

    print image_info['result']
