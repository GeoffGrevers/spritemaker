#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" creates a sprite from reference images """

__author__ = "Geoff Grevers"

from PIL import Image
import glob
import os, sys, math, time

frames = []
tileWidth = 0
tileHeight = 0

spritesheetWidth = 0
spritesheetHeight = 0

size = (16, 16)
images = glob.glob('files/*.ico')
images.sort() # alphabetize
frames = []
maxSpritesRow = math.ceil(math.sqrt(len(images)))

textFile = open("coodinates.txt","w+")
textFile.write("coordinates are in (x,y) format, where top left of the image is it's location \n")

# convert the icos into pngs of size 16 by 16
for infile in images:
    f, e = os.path.splitext(infile)
    outfile = f + ".png"

    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size)
            im.convert('RGBA')
            if im.mode == 'P':
                outfile = f + ".jpg"
                im.save(outfile, "JPEG")
                im.convert('RGBA')
                frames.append(im.getdata())
            else:
                im.save(outfile, "PNG")
                frames.append(im.getdata())
        except IOError:
            print("conversion error: cannot convert", infile)

# calculate the size of the spritesheet
tileWidth = frames[0].size[0]
tileHeight = frames[0].size[1]

if len(frames) > maxSpritesRow :
    spritesheetWidth = tileWidth * maxSpritesRow
    requiredRows = math.ceil(len(frames)/maxSpritesRow)
    spritesheetHeight = tileHeight * requiredRows
else:
    spritesheetWidth = tileWidth*maxSpritesRow
    spritesheetHeight = spritesheetWidth

spritesheet = Image.new("RGBA",(int(spritesheetWidth), int(spritesheetHeight)))

i = 0
for currentFrame in frames:
    try:
        top = tileHeight * math.floor((frames.index(currentFrame))/maxSpritesRow)
        left = tileWidth * (frames.index(currentFrame) % maxSpritesRow)
        bottom = top + tileHeight
        right = left + tileWidth

        box = (left,top,right,bottom)
        box = [int(i) for i in box]
        cutFrame = currentFrame.crop((0,0,tileWidth,tileHeight))

        spritesheet.paste(cutFrame, box)

        # print coordinates to a file
        f, e = os.path.splitext(images[i])
        textFile.write(str(f) + ': ' + str(int(left)) + ',' + str(top) + '\n')

        i += 1

    except IOError:
        print("cannot paste image")

textFile.close()
spritesheet.save("spritesheet" + time.strftime("%Y-%m-%dT%H-%M-%S") + ".png", "PNG")
