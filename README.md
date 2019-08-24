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

## viewer.py
`
python viewer.py input_dir [start_index]
`
Display images one by one from a directory.

### key bindings
`
space
` Pause/Resume slide show.

`
a
` Previews image.

`
d
` Next image.

`
p
` Log the image path to the console

## timelapse.sh
Naive shell script to capture pictures every second from a camera behind an http web server.

`
./timelapse.sh <output directory> <url>
`

## cams.exs
Script in elixir to take snapshots by a set interval from multiple cameras.
Supports initializing the cameras after crashes or disconnects
`
elixir cams.exs
`
