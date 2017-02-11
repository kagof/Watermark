# Watermark 

**Copyright (c) 2017 Karl Goffin**

Released under the MIT Open Source license.

<p align="center"><img src="exampleWatermark.jpg" height="400" /><img src="exampleWatermark2.jpg" height="400" /></p>

This is a verbose Python3 script for adding watermarks to images. It assumes you have a lighter version and a darker version of your watermark, and chooses which one to use based on how dark the image is where the watermark will go. Currently you have a choice of putting it in any of the corners. There are also several different ways to save the file. All options are detailed by running the script with the '--help' option.

I recently bought a DSLR and found myself wanting to put a non-obnoxious watermark on my photos. A quick Google search told me that there was plenty of software for doing this, some of it free, but I really didn't want to have to download something new. Additionally, I wanted to be able to put a watermark on a whole pile of photos, without having to deal with them in a GUI. So, I wrote a quick Python script, and ended up adding a decent amount of functionality to it.

It will require some tweaking to get it working on a system that isn't mine; I didn't plan to be releasing this. The areas that will need changing are noted in the comments. Additionally, you will require the *'pillow'* package for Python. You also need to have a watermark to use; I made mine in GIMP. This script calls for two versions, a light one and a dark one. Depending on how complex your logo is, you may just be able to invert the colours to create these two different versions.

This script now also requires your image to be a JPEG with EXIF data, or it will not run properly.