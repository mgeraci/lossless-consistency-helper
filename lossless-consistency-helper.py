#!/usr/bin/env python

from PIL import Image
import re
import os


# helpers
# ------------------------------------------------------------------------------

def get_depth(root, path):
    local_path = path.replace(root, '')
    return local_path.count(os.path.sep)

def add_error_to_res(section, key, error):
    if not res[section].get(key):
        res[section][key] = []

    res[section][key].append(error)


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
music_location = '/Volumes/Lossless/Lossless'
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

print 'Checking for missing covers, poorly formatted album covers, and empty folders...'

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
print 'Done! Check your results in output.txt'
print '<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3'
print ''
