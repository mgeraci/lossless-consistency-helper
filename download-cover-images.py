#!/usr/bin/env python

import os
import sys
import json
import requests
from localsettings import MUSIC_LOCATION

output_dir = os.path.dirname(os.path.realpath(__file__))
cover_dir = '{}/covers/'.format(output_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# helpers
# ------------------------------------------------------------------------------

def get_name_list_from_filename(path):
    '''
    Returns an list of [artist_name, album_name] from a file path.

    @param {str} path - the path of the album
    @return {list} - a list of [artist, album]
    '''

    res = path.replace(MUSIC_LOCATION, '')

    if res[0] == '/':
        res = res[1:]

    res = res.split('/')

    # discard any "cover.jpg", if present
    res = res[:2]

    return res

def download_image(folder, url):
    destination = '{}cover.png'.format(folder)
    print 'downloading {}'.format(destination)

    f = open(destination,'wb')
    f.write(requests.get(url).content)
    f.close()


# the script
# ------------------------------------------------------------------------------

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

    artist, album = get_name_list_from_filename(image)
    url = image_info['result']

    artist_dir = u'{}/covers/{}'.format(output_dir, artist)
    album_dir = u'{}/{}'.format(artist_dir, album)

    if not os.path.exists(artist_dir):
        os.makedirs(artist_dir)

    if not os.path.exists(album_dir):
        os.makedirs(album_dir)

    download_image(album_dir, url)

print ''
print 'Done! That wasn\'t too bad, right?'
print ''
