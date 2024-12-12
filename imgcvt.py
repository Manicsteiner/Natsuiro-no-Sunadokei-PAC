import os
import sys
import struct

from PIL import Image

def getFileNameWithoutExtension(path):
    return path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

def bin2png(file, saveDir='.'):
    fl = open(file, 'rb')
    filename = getFileNameWithoutExtension(file)
    fileDir = os.path.dirname(file) if saveDir == '.' else saveDir
    fl.seek(0x41C)
    width,height = struct.unpack("<2H", b'' + fl.read(4))
    width = width * 2
    height = height - 1
    img = Image.new('RGBA', (width, height))
    pixelColor = {}
    fl.seek(0x14)
    for i in range(256):
        color = fl.read(4)
        if (color[3] >= 0x80):
            alpha = 0xFF
        else:
            alpha = color[3] << 1
        pixelColor.update({i: (color[0], color[1], color[2], alpha)})
    fl.read(12)
    for y in range(height):
        for x in range(width):
            img.putpixel((x, y), pixelColor[fl.read(1)[0]])
    fl.close()
    img.save(fileDir + '/' + filename + '.png', 'png')
    print("bin2png: '" + file + "' convert png success! Save as '" + fileDir + '/' + filename + '.png' + "'")

if __name__ == '__main__':
    if len(sys.argv) < 2 :
        exit()
    files=[]
    files=sys.argv[1:]
    for file in files:
        bin2png(file, '.')
