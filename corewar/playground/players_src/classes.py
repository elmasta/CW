class Instruction:

    def __init__(self):
        self.toStore = []
        self.begin = []
        self.nmb_of_instruct = []
        self.desc = []
        self.instruct = []
        self.fileLines = []

    def CleanLines(self):
        temp = []
        for line in self.fileLines:
            string = line.split("#", 1)
            #print(string[0].isspace())
            if string[0].isspace() == False:
                if len(string[0]) > 0:
                    temp.append(string[0])
        self.fileLines = temp

    def Name(self):
        count = 4
        for line in self.fileLines:
            if ".name" in line:
                for i in range(len(line)):
                    if i > 6 and line[i] != '"':
                        self.begin.append(ord(line[i]))
                        count += 1
                    elif i > 6 and line[i] == '"':
                        break
        while count < 136:
            self.begin.append(0x00)
            count += 1

    def Description(self):
        count = 4
        for line in self.fileLines:
            if ".description" in line:
                for i in range(len(line)):
                    if i > 13 and line[i] != '"':
                        self.desc.append(ord(line[i]))
                        count += 1
                    elif i > 13 and line[i] == '"':
                        break
        while count < 2056:
            self.desc.append(0x00)
            count += 1

    def Instruct(self):
        label_list = []
        inst_list = []
        for i in range(len(self.fileLines)):
            #get the labels
            temp_str = ""
            for char in self.fileLines[i]:
                print(temp_str)
                if char == ":":
                    label_list.append({"name": temp_str, "origin": i})
                    temp_str = ""
                elif char != " " and char != "." and char != '\n':
                    temp_str += char
                else:
                    temp_str = ""
                    break
        for i in range(len(self.fileLines)):
            tempInst = []
            #check if line has label
            for sub_i in range(len(label_list)):
                if label_list[sub_i]["origin"] == i:
                    label_list[sub_i]["origin"] = len(inst_list)
                    break
            if "live" in self.fileLines[i]:
                # live 	1 	1 	10 	false 	false 	Direct
                tempInst.append(0x01)
                if self.fileLines[i][self.fileLines[i].index("%")+1] != ":": #no label
                    #3 zeros hardcoded because the argument is never a big number
                    tempInst.append(0x00)
                    tempInst.append(0x00)
                    tempInst.append(0x00)
                    ind = int(self.fileLines[i][self.fileLines[i].index("%")+1:])
                    tempInst.append(ind)
                else: #label
                    tempInst.append(0xff)
                    tempInst.append(0xff)
                    tempInst.append(0xff)
                    tempInst.append(ind)
            elif "ld" in self.fileLines[i]:
                # ld 	2 	2 	5 	true 	false 	[Indirect, Direct] Register
                opcode = 0
                tempInst.append(0x02)
                tempInst.append(0x00)
                splited = self.fileLines[i].split(",")
                pcount = 0
                for item in range(len(splited)):
                    splited_item = splited[item]
                    if item == 0:
                        first_splited = splited[0].split()
                        splited_item = first_splited[len(first_splited)-1]
                    #take this as example
                    if pcount == 0:
                        if splited_item[0] == "%":
                            opcode += 128
                        else:
                            opcode += 192
                    elif pcount == 1:
                        opcode += 16
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
                                temp_int = 4294967295+temp_int
                            temp_byte_calc = []
                            temp_byte_calc.append(temp_int%256)
                            temp_int = temp_int//256
                            temp_byte_calc.append(temp_int%256)
                            temp_int = temp_int//256
                            temp_byte_calc.append(temp_int%256)
                            temp_byte_calc.append(temp_int//256)
                            for ri in reversed(range(len(temp_byte_calc))):
                                tempInst.append(temp_byte_calc[ri])
                tempInst[1] = opcode

            elif "st" in self.fileLines[i] and "sti" not in self.fileLines[i]:
                # st 	2 	3 	5 	true 	false 	Register [Register, Indirect]
                opcode = 0
                tempInst.append(0x03)
                tempInst.append(0x00)
                splited = self.fileLines[i].split(",")
                for item in range(len(splited)):
                    splited_item = splited[item]
                    if item == 0:
                        first_splited = splited[0].split()
                        splited_item = first_splited[len(first_splited)-1]
                    if opcode == 0:
                        opcode = 64
                    elif opcode == 64:
                        if splited_item[0] == "r":
                            opcode += 16
                        else:
                            opcode += 48
                    else:
                        opcode += 4
                    if ":" in splited_item:
                        #label
                        tempInst.append(splited_item[1:])
                        tempInst.append(0)
                        tempInst.append(0)
                        tempInst.append(0)
                    else:
                        if "r" in splited_item:
                            splited_item = splited_item.replace('r', '')
                            tempInst.append(int(splited_item))
                        else:
                            temp_int = int(splited_item)
                            if temp_int < 0:
                                temp_int = 4294967295+temp_int
                            temp_byte_calc = []
                            temp_byte_calc.append(temp_int%256)
                            temp_int = temp_int//256
                            temp_byte_calc.append(temp_int%256)
                            temp_int = temp_int//256
                            temp_byte_calc.append(temp_int%256)
                            temp_byte_calc.append(temp_int//256)
                            for ri in reversed(range(len(temp_byte_calc))):
                                tempInst.append(temp_byte_calc[ri])
                tempInst[1] = opcode

            elif "add" in self.fileLines[i]:
                # add 	3 	4 	10 	true 	false 	Register Register Register
                tempInst.append(0x04)
            elif "sub" in self.fileLines[i]:
                # sub 	3 	5 	10 	true 	false 	Register Register Register
                tempInst.append(0x05)

            elif "and" in self.fileLines[i]:
                # and 	3 	6 	6 	true 	false 	[Register, Indirect, Direct] [Register, Indirect, Direct] Register
                opcode = 0
                tempInst.append(0x06)
                tempInst.append(0x00)
                splited = self.fileLines[i].split(",")
                for item in range(len(splited)):
                    splited_item = splited[item]
                    if item == 0:
                        first_splited = splited[0].split()
                        splited_item = first_splited[len(first_splited)-1]
                    if opcode == 0:
                        opcode = 64
                    elif opcode == 64:
                        if splited_item[0] == "%":
                            opcode += 32
                        elif splited_item[0] == "r":
                            opcode += 16
                        else:
                            opcode += 48
                    else:
                        if splited_item[0] == "%":
                            opcode += 8
                        else:
                            opcode += 4
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
                                temp_int = 4294967295+temp_int
                            temp_byte_calc = []
                            temp_byte_calc.append(temp_int%256)
                            temp_int = temp_int//256
                            temp_byte_calc.append(temp_int%256)
                            temp_int = temp_int//256
                            temp_byte_calc.append(temp_int%256)
                            temp_byte_calc.append(temp_int//256)
                            for ri in reversed(range(len(temp_byte_calc))):
                                tempInst.append(temp_byte_calc[ri])
                tempInst[1] = opcode

            elif "or" in self.fileLines[i] and "xor" not in self.fileLines[i]:
                # or 	3 	7 	6 	true 	false 	[Register, Indirect, Direct] [Register, Indirect, Direct] Register
                tempInst.append(0x07)
            elif "xor" in self.fileLines[i]:
                # xor 	3 	8 	6 	true 	false 	[Register, Indirect, Direct] [Register, Indirect, Direct] Register
                tempInst.append(0x08)

            elif "zjmp" in self.fileLines[i]:
                # zjmp 	1 	9 	20 	false 	true 	Direct
                tempInst.append(0x09)
                if self.fileLines[i][self.fileLines[i].index("%")+1] != ":": #no label
                    tempInst.append(0x00)
                    ind = int(self.fileLines[i][self.fileLines[i].index("%")+1:])
                    tempInst.append(ind)
                else: #label
                    testi = self.fileLines[i].index(":")+1
                    while testi != len(self.fileLines[i]):
                        if self.fileLines[i][testi] == "," or testi+1 == len(self.fileLines[i]):
                            label = self.fileLines[i][self.fileLines[i].index(":")+1:testi+1]
                            tempInst.append(label)
                            break
                        testi += 1
                    tempInst.append(0x00)

            elif "ldi" in self.fileLines[i]:
                # ldi 	3 	10 	25 	true 	true 	[Register, Indirect, Direct] [Register, Direct] Register
                tempInst.append(0x0a)

            elif "sti" in self.fileLines[i]:
                # sti 	3 	11 	25 	true 	true 	Register [Register, Indirect, Direct] [Register, Direct]
                opcode = 0
                tempInst.append(0x0b)
                tempInst.append(0x00)
                splited = self.fileLines[i].split(",")
                for item in range(len(splited)):
                    splited_item = splited[item]
                    if item == 0:
                        first_splited = splited[0].split()
                        splited_item = first_splited[len(first_splited)-1]
                    if opcode == 0:
                        opcode = 64
                    elif opcode == 64:
                        if splited_item[0] == "%":
                            opcode += 32
                        elif splited_item[0] == "r":
                            opcode += 16
                        else:
                            opcode += 48
                    else:
                        if splited_item[0] == "%":
                            opcode += 8
                        else:
                            opcode += 4
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
                tempInst[1] = opcode

            elif "fork" in self.fileLines[i] and "lfork" not in self.fileLines[i]:
                # fork 	1 	12 	800 	false 	true 	Direct
                tempInst.append(0x0c)
            elif "lld" in self.fileLines[i] and "lldi" not in self.fileLines[i]:
                # lld 	2 	13 	10 	true 	false 	[Indirect, Direct] Register
                tempInst.append(0x0d)
            elif "lldi" in self.fileLines[i]:
                # lldi 	3 	14 	50 	true 	true 	[Register, Indirect, Direct] [Register, Direct]
                tempInst.append(0x0e)
            elif "lfork" in self.fileLines[i]:
                # lfork 	1 	15 	1000 	false 	true 	Direct
                tempInst.append(0x0f)

            elif "nop" in self.fileLines[i]:
                # nop 	1 	16 	2 	true 	false 	Register
                opcode = 0
                tempInst.append(0x10)
                tempInst.append(0x00)
                splited = self.fileLines[i].split(",")
                for item in range(len(splited)):
                    splited_item = splited[item]
                    if item == 0:
                        first_splited = splited[0].split()
                        splited_item = first_splited[len(first_splited)-1]
                    if opcode == 0:
                        opcode = 64
                    elif opcode == 64 and splited_item[0] == "r":
                        opcode += 16
                    if ":" in splited_item:
                        #label
                        tempInst.append(splited_item[1:])
                        tempInst.append(0)
                        tempInst.append(0)
                        tempInst.append(0)
                    else:
                        if "r" in splited_item:
                            splited_item = splited_item.replace('r', '')
                            tempInst.append(int(splited_item))
                        else:
                            temp_int = int(splited_item)
                            if temp_int < 0:
                                temp_int = 4294967295+temp_int
                            temp_byte_calc = []
                            temp_byte_calc.append(temp_int%256)
                            temp_int = temp_int//256
                            temp_byte_calc.append(temp_int%256)
                            temp_int = temp_int//256
                            temp_byte_calc.append(temp_int%256)
                            temp_byte_calc.append(temp_int//256)
                            for ri in reversed(range(len(temp_byte_calc))):
                                tempInst.append(temp_byte_calc[ri])
                tempInst[1] = opcode

            if len(tempInst) > 0:
                inst_list.append(tempInst)
        for items in range(len(inst_list)):
            for item in range(len(inst_list[items])):
                if type(inst_list[items][item]) is str:
                    for label in label_list:
                        if label["name"] == inst_list[items][item]:
                            if inst_list[items][0] == 9 or inst_list[items][0] == 10\
                                or inst_list[items][0] == 11 or inst_list[items][0] == 12\
                                or inst_list[items][0] == 14 or inst_list[items][0] == 15:
                                #2 bytes
                                count = 0
                                if items > label["origin"]:
                                    cursor = items-1
                                    while cursor >= label["origin"]:
                                        count += len(inst_list[cursor])
                                        cursor -= 1
                                    count = count*-1
                                else:
                                    cursor = 0
                                    while cursor != label["origin"]:
                                        count += len(inst_list[cursor])
                                        cursor += 1
                                if count < 0:
                                    count = 65536+count
                                inst_list[items][item] = count//256
                                inst_list[items][item+1] = count%256
                                
                            else:
                                count = 0
                                if items > label["origin"]:
                                    cursor = items-1
                                    while cursor >= items:
                                        count += len(inst_list[cursor])
                                        cursor -= 1
                                    count += count*-1
                                else:
                                    cursor = 0
                                    while cursor != items:
                                        count += len(inst_list[cursor])
                                        cursor += 1
                                if count < 0:
                                    temp_int = 4294967295+temp_int
                                temp_byte_calc = []
                                temp_byte_calc.append(count%256)
                                count = count//256
                                temp_byte_calc.append(count%256)
                                count = count//256
                                temp_byte_calc.append(count%256)
                                temp_byte_calc.append(count//256)
                                count = 0
                                for ri in reversed(range(len(temp_byte_calc))):
                                    inst_list[items][item+count] = (temp_byte_calc[ri])
                                    count += 1
        for l in inst_list:
            for item in l:
                self.instruct.append(item)

    def regroup(self):
        self.toStore = self.begin + self.nmb_of_instruct + self.desc + self.instruct

    # def live(self):

    # def ld(self):

    # def st(self):

    # def add(self):

    # def sub(self):

    # def andd(self):

    # def orr(self):

    # def xor(self):

    # def zjmp(self):

    # def ldi(self):

    # def sti(self):

    # def fork(self):

    # def lld(self):

    # def lldi(self):

    # def lfork(self):

    # def nop(self):