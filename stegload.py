#!/usr/bin/env python3
# Author: Scragg
# Date: 17/05/2022
# Stegload is a tool used to load text data into a png file and extract it later.

from PIL import Image
import sys, getopt
import numpy as np
import binascii as ba

def main():
    # --------- Get arguments ---------
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hx:l:d:o:",["extract=","load=","data=","out="])
        for opt, arg in opts:
            if opt == '-h':
                print('Load Data: stegload -l <image_file> -d <data_file>')
                print('Extract Data: stegload -x <image_file> -o <output_file>\n')
                sys.exit()
    except getopt.GetoptError:
        print('USAGE:\n\tLoad Data: stegload -l <image_file> -d <data_file>')
        print('\tExtract Data: stegload -x <image_file> -o <output_file>\n')
        sys.exit(2)
        
    # --------- Check if arguments are a valid set ---------
    if (not (len(opts) == 2 and ((opts[0][0] == '-l' and opts[1][0] == '-d') or (opts[0][0] == '-x' and opts[1][0] == '-o')))):
        print('USAGE:\n\tLoad Data: stegload -l <image_file> -d <data_file>')
        print('\tExtract Data: stegload -x <image_file> -o <output_file>\n')
    else:
        print("+----------+\n| STEGLOAD |\n+----------+")
        if(opts[0][0] == '-l'):
            loadData(opts[0][1], opts[1][1])
        elif(opts[0][0] == '-x'):
            extractData(opts[0][1], opts[1][1])
        else:
            print("Unknown error please try again...")
            sys.exit(2)
        print("+--------------------+")
        print("| Operation Complete |")
        print("+--------------------+")

# --------- LOAD DATA INTO IMAGES ---------
def loadData(imgPath, dataPath):
    try:
        initialImage = Image.open(imgPath)
        data = open(dataPath).read()
    except Exception as e:
        print(e)
        print("Error loading files, please check paths and try again.")
        sys.exit(2)

    # --------- Get binary data ---------
    binData = ""
    for c in data:
        cBin = "0"+str(bin(int(ba.hexlify(bytes(c, 'utf8')), 16)))[2::]
        while(len(cBin) < 8):
            cBin = "0" + cBin
        binData = binData + cBin
    binData = binData+"00000011" # sentinel value (marks the end of our data)

    # --------- Print binary payload ---------
    print("Binary payload:\n-----------------")
    for i, c in enumerate(binData):
        if(i%8 == 0):
            print(" "+c, end="")
        else:
            print(c, end="")
    print("\n")

    # --------- Image processing ---------
    byteIdx = 0
    tmpImg = initialImage.convert('RGB')
    pixels = np.array(tmpImg)
    testBits = []
    for l, line in enumerate(pixels):
        for p, pix in enumerate(line):
            for i in range(0,3):
                if(len(binData) <= byteIdx):
                    break
                if(str(bin(pix[i]))[-1] != binData[byteIdx]):
                    if(str(bin(pix[i]))[-1] == "0"):
                        pixels[l][p][i]+=1
                    else:
                        pixels[l][p][i]-=1
                        
                byteIdx+=1

    # --------- Create image ---------
    res = Image.fromarray(pixels)
    res.save("out.png")
    res.close()
    initialImage.close()
    return

# --------- EXTRACT DATA FROM IMAGES ---------
def extractData(imgPath, outPath):
    try:
        initialImage = Image.open(imgPath)
        output = open(outPath, 'w')
    except:
        print("Error loading files, please check paths and try again.")
        sys.exit(2)

    # --------- Image processing ---------
    tmpImg = initialImage.convert('RGB')
    pixels = np.array(tmpImg)
    bits = []
    for l, line in enumerate(pixels):
        for p, pix in enumerate(line):
            for i in range(0,3):
                bits.append(str(bin(pix[i]))[-1])

    # --------- Convert bits to text ---------
    byte = ""
    data = ""
    for i, bit in enumerate(bits):
        if(len(byte) < 8):
            byte = byte+bit
        else:
            try:
                x = int(byte ,2)
                if(byte != '00000011'):
                    data = data+ba.unhexlify('%x' % x).decode("utf-8")
                else:
                    print(data)
                    break
            except Exception as e:
                data = data+"\n"
            byte = bit
    output.write(data)
    output.close()
    return

# --------- EXECUTE MAIN ON STARTUP ---------
if __name__ == "__main__":
    main()
