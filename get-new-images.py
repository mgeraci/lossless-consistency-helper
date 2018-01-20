#!/usr/bin/env python

import json
import os
from localsettings import MUSIC_LOCATION

output_dir = os.path.dirname(os.path.realpath(__file__))
data_file = 'output.txt'
import_file = '{}/{}'.format(output_dir, data_file)


print 'reading {} for data...'.format(import_file)

data = json.load(open(import_file))

for image in data['images']:
    print image
