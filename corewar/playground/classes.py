from extrafunc import *

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
                if char == ":":
                    label_list.append({"name": temp_str, "origin": i})
                    temp_str = ""
                elif char != " " and char != "." and char != '\n':
                    temp_str += char
                else:
                    temp_str = ""
                    break
        for i in range(len(self.fileLines)):
            if self.fileLines[i][0] != ".":
                tempInst = []
                #check if line has label
                for sub_i in range(len(label_list)):
                    if label_list[sub_i]["origin"] == i:
                        label_list[sub_i]["origin"] = len(inst_list)
                        break

                if "live" in self.fileLines[i]:
                    # live 	1 	1 	10 	false 	false 	Direct
                    tempInst.append(0x01)
                    splited = self.fileLines[i].split(",")
                    tempInst = ThirtyTwo(tempInst, splited, False)

                elif "ld" in self.fileLines[i]:
                    # ld 	2 	2 	5 	true 	false 	[Indirect, Direct] Register
                    tempInst.append(0x02)
                    splited = self.fileLines[i].split(",")
                    tempInst = ThirtyTwo(tempInst, splited, True)

                elif "st" in self.fileLines[i] and "sti" not in self.fileLines[i]:
                    # st 	2 	3 	5 	true 	false 	Register [Register, Indirect]
                    tempInst.append(0x03)
                    splited = self.fileLines[i].split(",")
                    tempInst = ThirtyTwo(tempInst, splited, True)

                elif "add" in self.fileLines[i]:
                    # add 	3 	4 	10 	true 	false 	Register Register Register
                    tempInst.append(0x04)
                    splited = self.fileLines[i].split(",")
                    tempInst = ThirtyTwo(tempInst, splited, True)

                elif "sub" in self.fileLines[i]:
                    # sub 	3 	5 	10 	true 	false 	Register Register Register
                    tempInst.append(0x05)
                    splited = self.fileLines[i].split(",")
                    tempInst = ThirtyTwo(tempInst, splited, True)

                elif "and" in self.fileLines[i]:
                    # and 	3 	6 	6 	true 	false 	[Register, Indirect, Direct] [Register, Indirect, Direct] Register
                    tempInst.append(0x06)
                    splited = self.fileLines[i].split(",")
                    tempInst = ThirtyTwo(tempInst, splited, True)

                elif "or" in self.fileLines[i] and "xor" not in self.fileLines[i]:
                    # or 	3 	7 	6 	true 	false 	[Register, Indirect, Direct] [Register, Indirect, Direct] Register
                    tempInst.append(0x07)
                    splited = self.fileLines[i].split(",")
                    tempInst = ThirtyTwo(tempInst, splited, True)

                elif "xor" in self.fileLines[i]:
                    # xor 	3 	8 	6 	true 	false 	[Register, Indirect, Direct] [Register, Indirect, Direct] Register
                    tempInst.append(0x08)
                    splited = self.fileLines[i].split(",")
                    tempInst = ThirtyTwo(tempInst, splited, True)

                elif "zjmp" in self.fileLines[i]:
                    # zjmp 	1 	9 	20 	false 	true 	Direct
                    tempInst.append(0x09)
                    splited = self.fileLines[i].split(",")
                    tempInst = Sixteen(tempInst, splited, False)

                elif "ldi" in self.fileLines[i]:
                    # ldi 	3 	10 	25 	true 	true 	[Register, Indirect, Direct] [Register, Direct] Register
                    tempInst.append(0x0a)
                    splited = self.fileLines[i].split(",")
                    tempInst = Sixteen(tempInst, splited, True)

                elif "sti" in self.fileLines[i]:
                    # sti 	3 	11 	25 	true 	true 	Register [Register, Indirect, Direct] [Register, Direct]
                    tempInst.append(0x0b)
                    splited = self.fileLines[i].split(",")
                    tempInst = Sixteen(tempInst, splited, True)

                elif "fork" in self.fileLines[i] and "lfork" not in self.fileLines[i]:
                    # fork 	1 	12 	800 	false 	true 	Direct
                    tempInst.append(0x0c)
                    splited = self.fileLines[i].split(",")
                    tempInst = Sixteen(tempInst, splited, False)

                elif "lld" in self.fileLines[i] and "lldi" not in self.fileLines[i]:
                    # lld 	2 	13 	10 	true 	false 	[Indirect, Direct] Register
                    tempInst.append(0x0d)
                    splited = self.fileLines[i].split(",")
                    tempInst = ThirtyTwo(tempInst, splited, True)

                elif "lldi" in self.fileLines[i]:
                    # lldi 	3 	14 	50 	true 	true 	[Register, Indirect, Direct] [Register, Direct]
                    tempInst.append(0x0e)
                    splited = self.fileLines[i].split(",")
                    tempInst = Sixteen(tempInst, splited, True)

                elif "lfork" in self.fileLines[i]:
                    # lfork 	1 	15 	1000 	false 	true 	Direct
                    tempInst.append(0x0f)
                    splited = self.fileLines[i].split(",")
                    tempInst = Sixteen(tempInst, splited, False)

                elif "nop" in self.fileLines[i]:
                    # nop 	1 	16 	2 	true 	false 	Register
                    tempInst.append(0x10)
                    splited = self.fileLines[i].split(",")
                    tempInst = ThirtyTwo(tempInst, splited, True)

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