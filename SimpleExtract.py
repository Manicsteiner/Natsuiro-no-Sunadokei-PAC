import os,sys,struct

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
            filename += ".tm2"
        wrfile = open("data/"+filename, 'wb')
        wrfile.write(readdata)
        wrfile.close()
        pl += 12
    print("Complete!")

def cstr(s):
    p = "{}s".format(len(s))
    s = struct.unpack(p,s)[0]
    return str(s.replace(b"\x00",b""),encoding = "sjis")

if __name__ =="__main__":
    main()

