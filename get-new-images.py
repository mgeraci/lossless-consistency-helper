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
import_file = '{}/{}'.format(output_dir, data_file)
api_url = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&format=json'
request_sleep = 5
json_parsing_codes = {
    'success': 0,
    'failure': 1,
}


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

    return res

def get_request_url(name_list):
    '''
    Create a request url for the last.fm api from an [artist, album] list.

    @param {list} name_list - a list of [artist, album]
    @return {str} - the request url
    '''

    # we need to add 3 things to the root url: api_key, artist, and album

    res = '{}&api_key={}&artist={}&album={}'.format(
        api_url,
        LAST_FM_API_KEY,
        urllib.quote(name_list[0].encode('utf-8')),
        urllib.quote(name_list[1].encode('utf-8')),
        )

    return res

def get_request_json(url):
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
    @return {number} res.code - a number indicating the success or failure
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
            'code': json_parsing_codes['failure'],
            'message': 'getting the image url from the api json failed'
        }

    return {
        'code': json_parsing_codes['success'],
        'result': image,
    }


# the script
# ------------------------------------------------------------------------------

res = {}

print ''
print 'COVER IMAGE FETCHING TIME'
print '-------------------------'
print ''

print 'reading {} for data...'.format(import_file)

try:
    data = json.load(open(import_file))
except:
    print 'output.txt was not found in this directory. did you run lossless-consistency-helper.py first?'
    sys.exit()

for image in data['images']:
    name_list = get_name_list_from_filename(image)
    request_url = get_request_url(name_list)

    print 'requesting {} - {}'.format(name_list[0], name_list[1])


    time.sleep(request_sleep)


# write the output
# ------------------------------------------------------------------------------

with open('{}/get-new-images-output.txt'.format(output_dir), 'w') as f:
    json.dump(res, f)
