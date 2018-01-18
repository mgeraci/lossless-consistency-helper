#!/usr/bin/env python

from PIL import Image
import re
import os


# "constants"
# ------------------------------------------------------------------------------

output_dir = os.path.dirname(os.path.realpath(__file__))
music_location = '/Volumes/Lossless/Lossless'
min_cover_dimension = 800


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
    success = False

    if 'cover.png' in items:
        success = 'cover.png'
    elif 'cover.jpg' in items:
        success = 'cover.jpg'
    elif 'cover.jpeg' in items:
        success = 'cover.jpeg'

    if success:
        return {
            'success': True,
            'filename': success,
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

    if i.size[0] != i.size[1]:
        errors.append('Image not square')

    if i.size[0] < min_cover_dimension or i.size[1] < min_cover_dimension:
        errors.append('Image too small')

    if len(errors):
        return {
            'success': False,
            'error': errors,
        }
    else:
        return { 'success': True }


# script
# ------------------------------------------------------------------------------

images = []
res = {
    'albums': {},
    'empty': {},
    'images': {},
}

print ''
print 'xxxxxxxxxxxxx'
print 'x hey there x'
print 'xxxxxxxxxxxxx'
print ''

os.chdir(music_location)

print 'Checking for missing covers, poorly formatted album folders, and empty folders...'

for root, dirnames, filenames in os.walk(music_location, topdown=True):
    depth = get_depth(music_location, root)

    # depth 0 = lossless root
    # depth 1 = artist
    # depth 2 = album

    # albums
    if depth == 1:
        if len(dirnames) == 0:
            add_error_to_res('empty', root, 'Empty folder')
        else:
            for album in dirnames:
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


print 'Checking the {} properly named images found for resolution and aspect ratio...'.format(len(images))

for image in images:
    image_check = check_image_size(image)

    if not image_check['success']:
        add_error_to_res('images', image, image_check['error'])

    print("."),


# write the output
# ------------------------------------------------------------------------------

with open('{}/output.txt'.format(output_dir), 'w') as f:
    for section in res:
        f.write('{}\n'.format(section))
        f.write('----------------------------\n')
        f.write('\n')

        for path in res[section]:
            errors = res[section][path]
            f.write('{} {}\n'.format(path, errors))

        f.write('\n')

print ''
print ''
print 'Done! Check your results in output.txt'
print '<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3'
print ''
