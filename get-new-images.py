#!/usr/bin/env python

import json
import os
import sys
import re
import urllib
import time
import requests
from localsettings import MUSIC_LOCATION, LAST_FM_API_KEY


# "constants"
# ------------------------------------------------------------------------------

output_dir = os.path.dirname(os.path.realpath(__file__))
data_file = 'output.txt'
api_url = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&format=json'
request_sleep = 1


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

    # scrub the year from the album name
    res[1] = re.sub(r'\d{4} - ', '', res[1])

    # some albums have "(Disc 1)" or "(Bonus disc)", etc.; kill those
    res[1] = re.sub(r'\((Disc|Bonus|Live).+?\)', '', res[1])

    return res

def get_request_url(artist, album):
    '''
    Create a request url for the last.fm api from an [artist, album] list.

    @param {str} artist - the album's artist
    @param {str} album - the artist's album
    @return {str} - the request url
    '''

    # we need to add 3 things to the root url: api_key, artist, and album
    res = '{}&api_key={}&artist={}&album={}'.format(
        api_url,
        LAST_FM_API_KEY,
        urllib.quote(artist.encode('utf-8')),
        urllib.quote(album.encode('utf-8')))

    return res

def make_json_request(url):
    '''
    Hit the given url and parse its response as json.

    @param {str} url - the url
    @return {dict} - the json returned by the url
    '''

    response = requests.get(url)
    return response.json()

def get_image_url_from_json(api_response):
    '''
    Given a response from the lastfm api, get an image url.

    @param {dict} api_response - a dict of info from the lastfm api
    @return {dict} res - a dictionary with the results
    @return {number} res.success - a number indicating the success or failure
    @return {str} [res.result] - the result, if successful
    @return {str} [res.message] - an error message, if failure
    '''

    try:
        images = api_response['album']['image']
        image = [i for i in images if i['size'] == 'mega'][0]
        image = image['#text']
        image = re.sub(r'\/\d{3}x\d{3}', '', image)
    except:
        return {
            'success': False,
            'message': 'getting the image url from the api json failed'
        }

    return {
        'success': True,
        'result': image,
    }


# the script
# ------------------------------------------------------------------------------

# get the data file
if len(sys.argv) == 1:
    print ''
    print 'This script must be passed a file to read data from, like `./get-new-images.py data.txt`'
    print ''
    sys.exit()

res = {}
got_rate_limited = False

print ''
print 'COVER IMAGE FETCHING TIME'
print '-------------------------'
print ''


import_file = '{}/{}'.format(output_dir, sys.argv[1])

print 'reading {} for data...'.format(import_file)

try:
    data = json.load(open(import_file))
except:
    print 'Your passed data file was either not found or corrupt.'
    sys.exit()


for image in data['images']:
    artist, album = get_name_list_from_filename(image)
    request_url = get_request_url(artist, album)

    print u'{} {} - {}'.format(
        'Skipping' if got_rate_limited else 'Requesting',
        artist,
        album)

    if got_rate_limited:
        res[image] = {
            'success': False,
            'message': 'Skipped by the script after an api error',
        }
    else:
        api_res = make_json_request(request_url)

        if api_res.get('error'):
            if api_res['error'] == 10:
                got_rate_limited = True
                print '- rate limit error; skipping the rest'
            elif api_res['error'] == 6:
                print '- no album match'
            else:
                print '- api error {}, see https://www.last.fm/api/errorcodes'.format(api_res['error'])

            res[image] = {
                'success': False,
                'message': 'Api error',
                'data': api_res,
            }
        else:
            print '- ok'

            res[image] = get_image_url_from_json(api_res)

            # sleep in between api requests to not get rate limited
            if not got_rate_limited:
                time.sleep(request_sleep)


# write the output
# ------------------------------------------------------------------------------

with open('{}/get-new-images-output.txt'.format(output_dir), 'w') as f:
    json.dump(res, f)
