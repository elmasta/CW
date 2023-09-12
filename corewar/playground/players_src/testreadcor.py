#chunk_size = 4096  # Define the size of each chunk in bytes

def main():
    # Read the binary file in chunks
    with open('ameba.cor', 'rb') as file:
        count = 0
        line = 0
        currentline = 0
        lineStorage = []
        byteStorage = []
        while (bytee := file.read(1)):
            if bytee != b'\x00':
                count += 1
            temp = ''.join(r'\x'+hex(letter)[2:] for letter in bytee)
            if len(temp) == 3:
                temp = temp[:2] + '0' + temp[2]
            byteStorage.append(bytee)
            lineStorage.append(temp)
            line += 1
            if line == 16:
                line = 0
                if count > 0:
                    for i in range(len(lineStorage)):
                        toPrint = "{:08b}".format(int(lineStorage[i][2:], base=16))
                        print("line", currentline, ": ",lineStorage[i] , "     bin :", toPrint, "                 ", byteStorage[i])
                    print()
                lineStorage.clear()
                byteStorage.clear()
                count = 0
                
                currentline += 1
    if len(lineStorage) > 0:
        for i in range(len(lineStorage)):
            toPrint = "{:08b}".format(int(lineStorage[i][2:], base=16))
            print("line", currentline, ": ",lineStorage[i] , "     bin :", toPrint, "                 ", byteStorage[i])

main()
