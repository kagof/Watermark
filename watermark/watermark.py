# Copyright (c) 2017 Karl Goffin
# Released under the MIT Open Source license.
# This is a verbose script for adding watermarks to images. It assumes you have a light and dark version of your logo,
# and chooses which one to use based on how dark the image is where the watermark will go. Currently you have a choice
# of putting it in any of the corners. There are several different ways to save the files. All options are detailed by
# running the script with the '--help' option.

# Written for Python 3.

import getopt
import sys
from os import path, listdir, mkdir
from time import sleep
from PIL import Image


# This other module just prevents me from writing an absolute
# path in my filesystem on Github. It contains a function which
# returns the absolute path to the watermark png files. It is used at the *~*~*~* symbol.
import logopaths


def main():
    overwrite = False
    new_folder = False
    only_new = False;
    is_folder = False
    position_set = False
    left_up = False
    right_up = False
    left_down = False
    right_down = True

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'onNf1234', ['help'])
        num_times = len(args)
        if num_times < 1 and '--help' not in [x[0] for x in opts]:
            print('usage: watermark [options] file1 [file2 ...]')
            exit(1)

    except getopt.GetoptError:
        print('Invalid option. Use --help for list of valid options.')
        exit(2)
    for opt, arg in opts:
        if opt == '-o':
            if new_folder:
                print('Overwrite and new folder options are incompatible.')
                exit(2)
            overwrite = True
            print('OVERWRITE WARNING: Original files will be overwritten. This cannot be undone. Press ctrl+C to stop.')
            print(str(3) + '....', end='')
            sys.stdout.flush()
            sleep(2)
            print(str(2) + '....', end='')
            sys.stdout.flush()
            sleep(2)
            print(str(1) + '....', end='')
            sys.stdout.flush()
            sleep(2)
            print(str(0) + '....', end='')
            sys.stdout.flush()
            sleep(2)
            print(' Continuing.')
        elif opt == '-n':
            if overwrite:
                print('Overwrite and new folder options are incompatible.')
                exit(2)
            new_folder = True
        elif opt == '-N':
            if overwrite:
                print('Overwrite and new folder options are incompatible.')
                exit(2)
            new_folder = True
            only_new = True  # note that if options -n and -N, program behave as if just -N option selected.
        elif opt == '-f':
            is_folder = True
        elif opt == '-1':
            if position_set:
                print('Watermark location already set.')
                exit(2)
            left_up = True
            right_down = False
            position_set = True
        elif opt == '-2':
            if position_set:
                print('Watermark location already set.')
                exit(2)
            right_up = True
            right_down = False
            position_set = True
        elif opt == '-3':
            if position_set:
                print('Watermark location already set.')
                exit(2)
            right_down = True
            position_set = True
        elif opt == '-4':
            if position_set:
                print('Watermark location already set.')
                exit(2)
            left_down = True
            right_down = False
            position_set = True
        elif opt == '--help':
            print('usage: watermark [options] file1 [file2 ...]')
            print('OPTIONS:')
            print('-o\t Turn on overwrite mode. Will overwrite the original file.')
            print('-n\t Save files to new child folder \'Watermarked\'.')
            print('-N\t Save files to new child folder \'Waterkarked\', ignoring files which are already there.')
            print('-f\t arg1 is a folder containing the images to be watermarked. Only reads arg1. Not recursive.\n')
            print('-1\t Print watermark in the upper left corner. Placed in bottom right by default.')
            print('-2\t Print watermark in the upper right corner. Placed in bottom right by default.')
            print('-3\t Print watermark in the bottom right corner. Placed in bottom right by default.')
            print('-4\t Print watermark in the bottom left corner. Placed in bottom right by default.\n')
            print('--help\t displays this help text.')
            sys.stdout.flush()
            exit(0)

    # *~*~*~*
    # Loading the watermarks. There is one which is dark and one
    # which is light, so that there is a suitable one for every file.
    # The logopaths module was just written to not have an absolute path
    # on my filesystem in the Github repository. You can replace it with
    # your own watermark .png file paths.
    watermark_dark = Image.open(logopaths.logopaths(1))
    watermark_light = Image.open(logopaths.logopaths(2))

    # -f option.
    if is_folder:
        folder_nm = args[0]
        if not path.isdir(folder_nm):
            print('Argument was not a folder name.')
            exit(1)
        if not folder_nm.endswith('/'):
            folder_nm += '/'
        # replace the list of arguments with the files in the folder.
        args = [folder_nm + f for f in listdir(folder_nm) if not (path.isdir(folder_nm + f))]
        num_times = len(args)

    err = 0

    for i in range(0, num_times):
        if only_new:  # -N check if file already is watermarked
            tail, head = path.split(args[i])
            filename, ext = path.splitext(head)
            if path.isfile(tail + '/Watermarked/' + filename + '_WM' + ext):
                print('Skipping image ' + str(i + 1) + ' of ' + str(num_times) + '.')
                continue

        print('Watermarking image ' + str(i + 1) + ' of ' + str(num_times) + '........', end='')
        sys.stdout.flush()
        try:
            img = Image.open(args[i])
        except IOError:
            print('Error reading file \'' + args[i] + '\'.')
            sys.stdout.flush()
            err += 1
            continue

        info = img.info  # ensures we can retrieve file information.

        # finding which corner the logo is to be placed in. 490x220 are the dimensions of my watermark;
        # you will want to change these numbers to match your dimensions.
        if right_down:
            x, y = img.width - 490, img.height - 220
            logo_area = img.crop((x, y, img.width, img.height))

        elif left_down:
            x, y = 0, img.height - 220
            logo_area = img.crop((x, y, 490, img.height))

        elif right_up:
            x, y = img.width - 490, 0
            logo_area = img.crop((x, y, img.width, 220))

        elif left_up:
            x, y = 0, 0
            logo_area = img.crop((x, y, 490, 220))

        # check if logo corner is dark, to decide whether to use light or dark watermark.
        # thanks, http://stackoverflow.com/a/27868513
        pixels = logo_area.getdata()
        num_black = 0
        for pixel in pixels:
            if (pixel[0] + pixel[1] + pixel[2]) < 125:  # you may want to tweak this value to suit your watermark.
                num_black += 1
        n = len(pixels)

        if (num_black / float(n)) > 0.47:  # you may want to tweak this value to suit your watermark as well.
            img.paste(watermark_light, (x, y), watermark_light)
            print('Done (light)')
            sys.stdout.flush()
        else:
            img.paste(watermark_dark, (x, y), watermark_dark)
            print('Done (dark)')
            sys.stdout.flush()



        # different save file options
        if overwrite:  # -o
            img.save(args[i], icc_profile=info['icc_profile'], subsampling='keep', adobe=('adobe' in info), qtables='keep', quality=100, exif=info['exif'])
        elif new_folder:  # -n or -N
            tail, head = path.split(args[i])
            filename, ext = path.splitext(head)
            img.save(tail + '/Watermarked/' + filename + '_WM' + ext, icc_profile=info['icc_profile'], subsampling='keep', adobe=('adobe' in info), qtables='keep', quality=100, exif=info['exif'])

        else:  # vanilla
            filename, ext = path.splitext(args[i])
            img.save(filename + '_WM' + ext, icc_profile=info['icc_profile'], subsampling='keep', adobe=('adobe' in info), qtables='keep', quality=100, exif=info['exif'])

    print(str(num_times - err) + '/' + str(num_times) + ' files successfully watermarked.')
if __name__ == '__main__':
    main()
