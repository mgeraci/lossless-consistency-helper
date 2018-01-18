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
```

Album year must be a 4-digit number. The cover must not be corrupt, and must be
a square of at least 800x800px (this can be modified in the script).


## Installation

* clone the repo
* `mkvirtualenv lossless-consistency-helper`
* `brew install libjpeg` if you don't have libjpeg installed
* `xcode-select --install` if you don't have the mac command-line tools install
* `pip install -r requirements.txt`


## Running the script

First, make sure you're in the virtualenv for this project with
`workon lossless-consistency-helper`. Then you can run the script with
`./lossless-image-helper.py`. It will write the results to output.txt.
