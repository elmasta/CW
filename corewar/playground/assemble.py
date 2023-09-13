from classes import *
import sys

def main():
    toStoreC = Instruction()
    toStoreC.begin.append(0x00)
    toStoreC.begin.append(0xea)
    toStoreC.begin.append(0x83)
    toStoreC.begin.append(0xf3)
    f = open("./players_src/"+sys.argv[1], 'r')
    toStoreC.fileLines = f.readlines()
    f.close()
    toStoreC.CleanLines()
    toStoreC.Name()
    toStoreC.Description()
    toStoreC.Instruct()
    temp = len(toStoreC.instruct)
    #the 4 bytes before description, are equals to number of bytes in countInstruct
    toStoreC.nmb_of_instruct.append(0)
    toStoreC.nmb_of_instruct.append(0)
    toStoreC.nmb_of_instruct.append(0)
    toStoreC.nmb_of_instruct.append(temp)
    toStoreC.regroup()
    #print(toStoreC.toStore)

    line = 0
    lineStorage = []
    f = open("./players_src/test.cor", "wb")
    for i in toStoreC.toStore:
        if line == 16:
            print(lineStorage)
            toWrite = bytearray(lineStorage)
            f.write(toWrite)
            lineStorage.clear()
            line = 0
        lineStorage.append(i)
        line += 1
    if len(lineStorage) > 0:
        toWrite = bytearray(lineStorage)
        f.write(toWrite)
        print(lineStorage)
    f.close()
        
main()