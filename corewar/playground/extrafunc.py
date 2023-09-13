def ThirtyTwo(tempInst, splited, has_pcode):
    pcode = 0
    pcount = 0
    if has_pcode:
        tempInst.append(0x00)
    for item in range(len(splited)):
        splited_item = splited[item]
        if item == 0:
            first_splited = splited[0].split()
            splited_item = first_splited[len(first_splited)-1]
        splited_item = splited_item.replace(" ", "")
        if has_pcode:
            if pcount == 0:
                if splited_item[0] == "%":
                    pcode += 128
                elif splited_item[0] == "r":
                    pcode += 64
                else:
                    pcode += 192
            elif pcount == 1:
                if splited_item[0] == "%":
                    pcode += 32
                elif splited_item[0] == "r":
                    pcode += 16
                else:
                    pcode += 48
            elif pcount == 2:
                if splited_item[0] == "%":
                    pcode += 8
                elif splited_item[0] == "r":
                    pcode += 4
                else:
                    pcode += 12
            pcount += 1
        if ":" in splited_item:
            #label
            if "%" in splited_item:
                tempInst.append(splited_item[2:])
            else:
                tempInst.append(splited_item[1:])
            tempInst.append(0)
            tempInst.append(0)
            tempInst.append(0)
        else:
            splited_item = splited_item.replace('%', '')
            if "r" in splited_item:
                splited_item = splited_item.replace('r', '')
                tempInst.append(int(splited_item))
            else:
                temp_int = int(splited_item)
                if temp_int < 0:
                    temp_int = 4294967296+temp_int
                temp_byte_calc = []
                temp_byte_calc.append(temp_int%256)
                temp_int = temp_int//256
                temp_byte_calc.append(temp_int%256)
                temp_int = temp_int//256
                temp_byte_calc.append(temp_int%256)
                temp_byte_calc.append(temp_int//256)
                for ri in reversed(range(len(temp_byte_calc))):
                    tempInst.append(temp_byte_calc[ri])
    if has_pcode:
        tempInst[1] = pcode
    return tempInst

def Sixteen(tempInst, splited, has_pcode):
    pcode = 0
    pcount = 0
    if has_pcode:
        tempInst.append(0x00)
    for item in range(len(splited)):
        splited_item = splited[item]
        if item == 0:
            first_splited = splited[0].split()
            splited_item = first_splited[len(first_splited)-1]
        splited_item = splited_item.replace(" ", "")
        if has_pcode:
            if pcount == 0:
                if splited_item[0] == "%":
                    pcode += 128
                elif splited_item[0] == "r":
                    pcode += 64
                else:
                    pcode += 192
            elif pcount == 1:
                if splited_item[0] == "%":
                    pcode += 32
                elif splited_item[0] == "r":
                    pcode += 16
                else:
                    pcode += 48
            elif pcount == 2:
                if splited_item[0] == "%":
                    pcode += 8
                elif splited_item[0] == "r":
                    pcode += 4
                else:
                    pcode += 12
            pcount += 1
        if ":" in splited_item:
            #label
            if "%" in splited_item:
                tempInst.append(splited_item[2:])
            else:
                tempInst.append(splited_item[1:])
            tempInst.append(0)
        else:
            splited_item = splited_item.replace('%', '')
            if "r" in splited_item:
                splited_item = splited_item.replace('r', '')
                tempInst.append(int(splited_item))
            else:
                temp_int = int(splited_item)
                if temp_int < 0:
                    # 256*xxx/2 calcul 16bit
                    # 128 in second byte is first negative
                    # 256*128 == -32768
                    # how to find the number example for -32768: 256*128 - (256*256)
                    temp_int = 65536+temp_int
                tempInst.append(temp_int//256)
                tempInst.append(temp_int%256)
    if has_pcode:
        tempInst[1] = pcode
    return tempInst