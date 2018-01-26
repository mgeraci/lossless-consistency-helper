# Lossless Consistency Helper

This is a simple script to check my Flac music collection for consistency. I
have a few requirements for how my music is named and organized, so this script
outputs a list of items to fix.


## What it looks for

My desired folder structure is as follows:

```
root
|_ artist_name
   |_ album_year - album_title
      |_ cover.[png|jpg|jpeg]
      |_ artist - year - album - tracknumber - songtitle
```

Album year must be a 4-digit number. The cover must not be corrupt, and must be
a square of at least 800x800px (this can be modified in the script).


## Installation

* clone the repo
* `mkvirtualenv lossless-consistency-helper`
* `brew install libjpeg` if you don't have libjpeg installed
* `xcode-select --install` if you don't have the mac command-line tools install
* `pip install -r requirements.txt`
* add a file called `localsettings.py`, with the following information:

```
MUSIC_LOCATION = '/michaels/sick/tunez'
LAST_FM_API_KEY = '[get your key from the last.fm developer portal]'
```


## Running the script

First, make sure you're in the virtualenv for this project with
`workon lossless-consistency-helper`. Then you can run the script with
`./lossless-consistency-helper.py`. It will write the results to
lossless-consistency-helper-output.txt.

Next, if you would like to automate the fetching of new cover images, you should
run `./get-new-images.py lossless-consistency-helper-output.txt`. That will look
for the image-related results of the previous script, then try searching the
Last.FM API for a new image url.

After that, you can run `./download-cover-images.py` to run through the previous
script's results, and actually download the images. They'll get put into a
directory in the folder called `covers`.

And finally, run `./move-downloaded-images.py` to put the newly downloaded
images into place.
