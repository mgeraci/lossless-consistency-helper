#!/usr/bin/env python

from PIL import Image
import json
import re
import os
from localsettings import MUSIC_LOCATION


# "constants"
# ------------------------------------------------------------------------------

output_dir = os.path.dirname(os.path.realpath(__file__))
min_cover_dimension = 500


# helpers
# ------------------------------------------------------------------------------

def get_depth(root, path):
    local_path = path.replace(root, '')
    return local_path.count(os.path.sep)

def add_error_to_res(section, key, error):
    if not res[section].get(key):
        res[section][key] = []

    res[section][key].append(error)

def check_album_folder(path):
    if re.search("^\d{4} - .+", path):
        return { 'success': True }
    else:
        return {
            'success': False,
            'error': 'Bad album folder name'
        }

def check_for_cover(items):
    res = []

    if 'cover.png' in items:
        res.append('cover.png')

    if 'cover.jpg' in items:
        res.append('cover.jpg')

    if 'cover.jpeg' in items:
        res.append('cover.jpeg')

    if len(res) > 1:
        return {
            'success': False,
            'error': 'Multiple images found named "cover"'
        }
    if len(res) == 1:
        return {
            'success': True,
            'filename': res[0],
        }
    else:
        return {
            'success': False,
            'error': 'Missing cover image'
        }

def check_image_size(image):
    try:
        i = Image.open(image)

    except:
        return {
            'success': False,
            'error': 'Could not open image file',
        }

    errors = []

    '''
    if i.size[0] != i.size[1]:
        errors.append('Image not square')
    '''

    if i.size[0] < min_cover_dimension or i.size[1] < min_cover_dimension:
        errors.append('Image too small')

    if len(errors):
        return {
            'success': False,
            'error': errors,
        }
    else:
        return { 'success': True }

def check_for_song(filenames):
    flac_files = [x for x in filenames if x.find('.flac') > 0]

    # if there are no flac files, return success
    if not len(flac_files):
        return { 'success': True }

    filename = flac_files[0]

    # test for "artist - year - album - track - title"
    if re.match(r'^.+? - \d{4} - .+? - \d+ - .+$', filename):
        return { 'success': True }
    else:
        return {
            'success': False,
            'error': 'Bad song filename',
        }


# script
# ------------------------------------------------------------------------------

album_count = 0
good_image_count = 0
images = []
res = {
    'albums': {},
    'empty': {},
    'images': {},
    'songs': {},
}

print ''
print 'xxxxxxxxxxxxx'
print 'x hey there x'
print 'xxxxxxxxxxxxx'
print ''

os.chdir(MUSIC_LOCATION)

print 'Checking for missing covers, poorly formatted album folders, and empty folders...'

for root, dirnames, filenames in os.walk(MUSIC_LOCATION, topdown=True):
    depth = get_depth(MUSIC_LOCATION, root)

    # depth 0 = lossless root
    # depth 1 = artist
    # depth 2 = album

    # albums
    if depth == 1:
        if len(dirnames) == 0:
            add_error_to_res('empty', root, 'Empty folder')
        else:
            for album in dirnames:
                album_count += 1
                album_check = check_album_folder(album)

                if not album_check['success']:
                    full_path = '{}/{}'.format(root, album)
                    add_error_to_res('albums', full_path, album_check['error'])

    # songs / art
    if depth == 2:
        has_cover_check = check_for_cover(filenames)

        if has_cover_check['success']:
            images.append('{}/{}'.format(root, has_cover_check['filename']))
        else:
            add_error_to_res('images', root, has_cover_check['error'])

        has_good_song_filename_check = check_for_song(filenames)

        if not has_good_song_filename_check['success']:
            add_error_to_res('songs', root, has_good_song_filename_check['error'])


print 'Checking the {} properly named images found for resolution and aspect ratio...'.format(len(images))

for image in images:
    image_check = check_image_size(image)

    if image_check['success']:
        good_image_count += 1
    else:
        add_error_to_res('images', image, image_check['error'])


# write the output
# ------------------------------------------------------------------------------

with open('{}/lossless-consistency-helper-output.txt'.format(output_dir), 'w') as f:
    json.dump(res, f)

print ''
print 'Done! Check your results in output.txt'
print '{} albums found, {} good images found ({}%)'.format(
    album_count,
    good_image_count,
    (float(good_image_count) / float(album_count)) * 100)
print '<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3'
print ''
