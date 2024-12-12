import os,sys,struct
from PIL import Image

def main():
    if not os.path.exists("PAC.PAC") or not os.path.exists("PAC.HED"):
        print("File not exist")
        return
    filedata = open("PAC.PAC", 'rb')
    filelist = open("PAC.HED", 'rb')
    datadata = b'' + filedata.read()
    datalist = b'' + filelist.read()
    pl = 0
    os.system("mkdir data")
    listsize = os.path.getsize("PAC.HED")
    while pl < listsize:
        filename,filestart,filelength = struct.unpack("<3I",datalist[pl:pl+12])
        readdata = datadata[filestart:filestart+filelength]
        filename = str(filename).zfill(5)
        if struct.unpack(">I",datadata[filestart:filestart+4])[0] == 0x54494D32:
            wrfile = open("data/" + filename + ".tm2", 'wb')
            wrfile.write(readdata)
            wrfile.close()
        else:
            width,height = struct.unpack("<2H", readdata[0x41C:0x420])
            width = width * 2
            height = height - 1
            img = Image.new('RGBA', (width, height))
            pixelColor = {}
            pin = 0x14
            for i in range(256):
                color = struct.unpack("4B", readdata[pin:pin+4])
                if (color[3] >= 0x80):
                    alpha = 0xFF
                else:
                    alpha = color[3] << 1
                pixelColor.update({i: (color[0], color[1], color[2], alpha)})
                pin += 4
            pin += 12
            for y in range(height):
                for x in range(width):
                    img.putpixel((x, y), pixelColor[readdata[pin]])
                    pin += 1
            img.save("data/" + filename + '.png', 'png')
        pl += 12
    print("Complete!")

def cstr(s):
    p = "{}s".format(len(s))
    s = struct.unpack(p,s)[0]
    return str(s.replace(b"\x00",b""),encoding = "sjis")

if __name__ =="__main__":
    main()
