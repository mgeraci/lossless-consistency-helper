#!/usr/bin/env python

from PIL import Image
import re
import os


# helpers
# ------------------------------------------------------------------------------

def add_error_to_res(style, key, error):
    if not res[style].get(key):
        res[style][key] = []

    res[style][key].append(error)


def check_filename(path):
    is_good_png = 'cover.png' in path
    is_good_jpg = 'cover.jpg' in path
    is_good_jpeg = 'cover.jpeg' in path

    if is_good_png or is_good_jpg or is_good_jpeg:
        return { 'success': True }
    else:
        return {
            'success': False,
            'error': 'Bad filename'
        }

def check_album_folder(path):
    if re.search("^\d{4} - .+", path):
        return { 'success': True }
    else:
        return {
            'success': False,
            'error': 'Bad album folder name'
        }

def check_for_cover(items):
    has_png = 'cover.png' in items
    has_jpg = 'cover.jpg' in items
    has_jpeg = 'cover.jpeg' in items

    if has_png or has_jpg or has_jpeg:
        return { 'success': True }
    else:
        return {
            'success': False,
            'error': 'Missing cover image'
        }


# script
# ------------------------------------------------------------------------------

output_dir = os.path.dirname(os.path.realpath(__file__))
path = '/Volumes/Lossless/Lossless'
res = {
    'albums': {},
    'empty': {},
    'images': {},
}

print 'xxxxxxxxxxxxx'
print 'x hey there x'
print 'xxxxxxxxxxxxx'
print ''

os.chdir(path)

for root, dirnames, filenames in os.walk(path, topdown=True):
    depth = root[len(path) + len(os.path.sep):].count(os.path.sep)

    # albums
    if depth == 0:
        if len(dirnames) == 0:
            add_error_to_res('empty', root, 'Empty folder')
        else:
            for album in dirnames:
                album_check = check_album_folder(album)

                if not album_check['success']:
                    full_path = '{}/{}'.format(root, album)
                    add_error_to_res('albums', full_path, album_check['error'])

    # songs / art
    if depth == 1:
        # print filenames
        has_cover_check = check_for_cover(filenames)

        if not has_cover_check['success']:
            add_error_to_res('images', root, has_cover_check['error'])


    '''
    for filename in filenames:
        is_png = '.png' in filename
        is_jpg = '.jpg' in filename
        is_jpeg = '.jpeg' in filename

        if is_png or is_jpg or is_jpeg:
            images.append(os.path.join(root, filename))
    '''


'''
for image in images:
    filename_check = check_filename(image)

    if not filename_check['success']:
        add_error_to_res('image', image, filename_check['error'])
'''

# print res['images']


# write the output
# ------------------------------------------------------------------------------

print output_dir

with open('{}/output.txt'.format(output_dir), 'w') as f:
    for section in res:
        f.write('{}\n'.format(section))
        f.write('----------------------------\n')
        f.write('\n')
