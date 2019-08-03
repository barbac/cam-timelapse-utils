# cam-timelapse-utils

## filter.py
Uses opencv to detect changes in a sequence of images and discards frames that are too similar.

### display the images on screen without saving anything:
`
python filter.py input_dir
`

### save the filtered images into a new directory:
`
python filter.py input_dir output_dir
`

## timelapse.sh
Naive shell script to capture pictures every second from a camera behind an http web server.

`
./timelapse.sh <output directory> <url>
`
