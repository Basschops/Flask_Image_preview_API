# Flask_Image_preview_API
Flask API that gives a preview of images from Pond5 as well as ping test and system information display.

This application has an API for three services. To display information about images from https://www.pond5.com/photo/ .
To ping the site and also to return system information.


This application is available through Docker using the command

  docker run -p 4000:80 dofarrell/pond5:part1

To build and run the application locally use teh following two commands

  docker build --tag=image_preview .

  docker run -p 4000:80 image_preview


When the application is running, the APIs can be accessed via the following routes

  navigate to localhost:4000/ping to ping Pond5 site.

  navigate to localhost:4000/system to display system information.

  navigate to localhost:4000/mediainfo/media_id to get preview information of an image, where media_id is the resource id number.
