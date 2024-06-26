import sys

reg_bin = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "FLAGS":7}
mem_bin = {}

#key is mem addr, value is instruction
insdict = {}

#label,var => key is var/label and value is memory address 
label_dict = {}
vardictionary = {}

#creating a decimal to binary converter which takes the decimal and the number of bits as input\
def returnbin(num,bits):
    s = bin(num)
    s = s[2:] 
    assert(len(s) <= bits),"number cannot be represented in given number of bits"
    for i in range(bits - len(s)):
        s = '0' + s
    return s

# creating dicts for opcodes
instruction_code = {'add':0,
         'sub':1,
         'mov_imm':2,
         'mov_reg':3,
         'ld':4,
         'st':5,
         'mul':6,
         'div':7,
         'rs':8,
         'ls':9,
         'xor':10,
         'or':11,
         'and':12,
         'not':13,
         'cmp':14,
         'jmp':15,
         'jlt':28,
         'jgt':29,
         'je':31,
         'hlt':26,
         'addf':16,
         'subf':17,
         'movf':18}

# creating dicts for types
types = {'add':"A",
         'sub':"A",
         'mov_imm':"B",
         'mov_reg':"C",
         'ld':"D",
         'st':"D",
         'mul':"A",
         'div':"C",
         'rs':"B",
         'ls':"B",
         'xor':"A",
         'or':"A",
         'and':"A",
         'not':"C",
         'cmp':"C",
         'jmp':"E",
         'jlt':"E",
         'jgt':"E",
         'je':"E",
         'hlt':"F",
         'addf':"A",
         'subf':"A",
         'movf':"B"}


#function for inserting vars in dict which takes line number, name as input
def validity_check_opcode(opcode):
    global instruction_code
    if opcode in instruction_code:
        return True
    else:
        return False
    
def validity_check_register(register):
    global reg_bin
    if register in reg_bin:
        return True
    else:
        return False
    
def validity_check_mem_address(mem_addr):
    global mem_bin
    if mem_addr in mem_bin:
        return True
    else:
        return False

def add_print(instruction):
    global instruction_code
    #checking validity
    temp_lst = instruction.split()
    if validity_check_opcode(temp_lst[0]) == False:
        s = "Invalid opcode"
        return s
    if len(temp_lst) != 4:
        s = "Number of arguments in addition instruction are invalid"
        return s
    for i in range(1,4):
        if validity_check_register(temp_lst[i]) == False:
            s = "Invalid registers"
            return s
    opcode_str = returnbin(instruction_code['add'],5)
    print_machine_code = opcode_str + "00" + returnbin(reg_bin[temp_lst[1]], 3) + returnbin(reg_bin[temp_lst[2]], 3) + returnbin(reg_bin[temp_lst[3]], 3)
    # print(print_machine_code)
    return print_machine_code

def sub_print(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    if validity_check_opcode(templst[0]) == False:
        s = "Invalid opcode"
        return s
    if len(templst) != 4:
        s = "Number of arguments in subtraction instruction are invalid"
        return s
    j = 1
    for i in range(3):
        if validity_check_register(templst[j]) == False:
            s = "Invalid register"
            return s
        j += 1
    opcodestr = returnbin(instruction_code['sub'],5)
    # print_machine_code = print_machine_code  + "00" + returnbin(reg_lst(templst[1]),3)+ returnbin(reg_lst(templst[2]),3)+ returnbin(reg_lst(templst[3]),3)
    print_machine_code = opcodestr + "00" + returnbin(reg_bin[templst[1]],3)+returnbin(reg_bin[templst[2]],3)+returnbin(reg_bin[templst[3]],3)
    # print(print_machine_code)
    return print_machine_code

def move_immediate(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    if validity_check_opcode(templst[0]) == False:
        s = "Invalid opcode"
        return s
    if len(templst) != 3:
        s = "Number of arguments in move_immediate instruction are invalid"
        return s
    if validity_check_register(templst[1]) == False:
        s = "Invalid register"
        return s
    imm = templst[2]
    imm = imm[1:]
    imm = int(imm)
    if imm < 0 or imm > 127:
        s = "Immediate value out of range"
        return s
    opcodestr = returnbin(instruction_code['mov_imm'], 5)
    print_machine_code = opcodestr +"0"+ returnbin(reg_bin[templst[1]], 3) + returnbin(imm, 7)
    # print(print_machine_code)
    return print_machine_code

def move_register(instruction):
    global instruction_code
    templst = instruction.split()
    if (validity_check_opcode(templst[0]) == False):
        s = "Invalid instruction"
        return s
    if len(templst) != 3:
        s = "Number of arguments in move_register instruction are invalid"
        return s
    for i in range(1,3):
        if validity_check_register(templst[i]) == False:
            s = "Invalid register"
            return s
    dest_reg = reg_bin.get(templst[1])
    src_reg = reg_bin.get(templst[2])
    dest_reg_bin = returnbin(dest_reg, 3)
    src_reg_bin = returnbin(src_reg, 3)
    print_machine_code = returnbin(instruction_code['mov_reg'], 5) + "00000" + dest_reg_bin + src_reg_bin
    # print(print_machine_code)
    return print_machine_code

def ld_print(instruction):
    global instruction_code
    temp_lst = instruction.split()
    if len(temp_lst) != 3:
        s = "Number of arguments in load instruction are invalid"
        return s
    if validity_check_opcode(temp_lst[0]) == False:
        s = "Invalid opcode"
        return s
    if validity_check_register(temp_lst[1]) == False:
        s = "Invalid register"
        return s
    if temp_lst[2] not in vardictionary:
        s = "var error"
        return s
    opcode_str = returnbin(instruction_code['ld'],5)
    print_machine_code = opcode_str + "0" + returnbin(reg_bin[temp_lst[1]], 3) + returnbin(vardictionary[temp_lst[2]], 7)
    # print(print_machine_code)
    return print_machine_code

def st_print(instruction):
    temp_lst = instruction.split()
    if len(temp_lst) != 3:
        s = "Number of arguments in store instruction are invalid"
        return s
    if validity_check_opcode(temp_lst[0]) == False:
        s = "Invalid opcode"
        return s
    if validity_check_register(temp_lst[1]) == False:
        s = "Invalid register"
        return s
    if temp_lst[2] not in vardictionary:
        s = "var error"
        return s
    opcode_str = returnbin(instruction_code['st'],5)
    print_machine_code = opcode_str + "0" + returnbin(reg_bin[temp_lst[1]], 3) + returnbin(vardictionary[temp_lst[2]], 7)
    # print(print_machine_code)
    return print_machine_code

def mul_print(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    if validity_check_opcode(templst[0]) == False:
        s = "Invalid opcode"
        return s
    if len(templst) != 4:
        s = "Number of arguments in multiply instruction are invalid"
        return s
    j = 1
    for i in range(3):
        if validity_check_register(templst[j]) == False:
            s = "Invalid register"
            return s
        j += 1
    opcodestr = returnbin(instruction_code['mul'],5)
    #print_machine_code = print_machine_code  + "00" + returnbin(reg_lst(templst[1]),3)+ returnbin(reg_lst(templst[2]),3)+ returnbin(reg_lst(templst[3]),3)
    print_machine_code = opcodestr + "00" + returnbin(reg_bin[templst[1]],3)+returnbin(reg_bin[templst[2]],3)+returnbin(reg_bin[templst[3]],3)
    # print(print_machine_code)
    return print_machine_code

def divide(instruction):
    global instruction_code
    lst = instruction.split()
    if (validity_check_opcode(lst[0]) == False):
        s = "Invalid opcode"
        return s
    if len(lst) != 3:
        s = "Number of arguments in division instruction are invalid"
        return s
    for i in range(1,3):
        if validity_check_register(lst[i]) == False:
            s = "Invalid register"
            return s
    dest_reg = reg_bin.get(lst[1])
    src_reg = reg_bin.get(lst[2])
    dest_reg_bin = returnbin(dest_reg, 3)
    src_reg_bin = returnbin(src_reg, 3)
    print_machine_code = returnbin(instruction_code['div'], 5) + "00000" + dest_reg_bin + src_reg_bin
    # print(print_machine_code)
    return print_machine_code

def rs_print(instruction):
    global instruction_code
    temp_lst = instruction.split()
    temp_lst[2] = temp_lst[2][1:]
    if len(temp_lst) != 3:
        s = "Number of arguments in right shift instruction are invalid"
        return s
    if validity_check_opcode(temp_lst[0]) == False:
        s = "Invalid opcode"
        return s
    if validity_check_register(temp_lst[1]) == False:
        s="Invalid register"
        return s
    # assert validity_check_imm(temp_lst[2]) == True, "Invalid immediate"
    imm = int(temp_lst[2])
    if imm < 0 or imm > 127:
        s = "Immediate value out of range"
        return s
    opcode_str = returnbin(instruction_code['rs'],5)
    print_machine_code = opcode_str + "0" + returnbin(reg_bin[temp_lst[1]], 3) + returnbin(imm, 7)
    # print(print_machine_code)
    return print_machine_code

def ls_print(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    if validity_check_opcode(templst[0]) == False:
        s = "Invalid opcode"
        return s
    if len(templst) != 3:
        s = "Number of argumnents in left shift instruction are invalid"
        return s
    if validity_check_register(templst[1]) == False:
        s = "Invalid register"
        return s
    imm = templst[2]
    imm = imm[1:]
    imm = int(imm)
    opcode_str = returnbin(instruction_code['ls'],5)
    print_machine_code = opcode_str + "0" + returnbin(reg_bin[templst[1]], 3) + returnbin(imm,7)
    # print(print_machine_code)
    return print_machine_code

def xor_print(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    if validity_check_opcode(templst[0]) == False:
        s = "Invalid opcode"
        return s
    if len(templst) != 4:
        s = "Number of arguments in XOR instruction are invalid"
        return s
    j = 1
    for i in range(3):
        if validity_check_register(templst[j]) == False:
            s = "Invalid register"
            return s
        j += 1
    opcodestr = returnbin(instruction_code['xor'],5)
    #print_machine_code = print_machine_code  + "00" + returnbin(reg_lst(templst[1]),3)+ returnbin(reg_lst(templst[2]),3)+ returnbin(reg_lst(templst[3]),3)
    print_machine_code = opcodestr + "00" + returnbin(reg_bin[templst[1]],3)+returnbin(reg_bin[templst[2]],3)+returnbin(reg_bin[templst[3]],3)
    # print(print_machine_code)
    return print_machine_code

def or_print(instruction):
    global instruction_code
    lst = instruction.split()
    if (validity_check_opcode(lst[0]) == False):
        s = "Invalid opcode"
        return s
    if len(lst) != 4:
        s = "Number of arguments in OR instruction are invalid"
        return s
    for i in range(1,4):
        if validity_check_register(lst[i]) == False:
            s = "Invalid registers"
            return s

    dest_reg = reg_bin.get(lst[1])
    src_reg1 = reg_bin.get(lst[2])
    src_reg2 = reg_bin.get(lst[3])

    dest_reg_bin = returnbin(dest_reg, 3)
    src_reg1_bin = returnbin(src_reg1, 3)
    src_reg2_bin = returnbin(src_reg2, 3)

    print_machine_code = returnbin(instruction_code['or'], 5) + "00" + dest_reg_bin + src_reg1_bin + src_reg2_bin
    # print(print_machine_code)
    return print_machine_code

def and_print(instruction):
    global instruction_code
    #checking validity
    temp_lst = instruction.split()
    if (validity_check_opcode(temp_lst[0]) == False):
        s = "Invalid opcode"
        return s
    if len(temp_lst) != 4:
        s = "Number of arguments in AND instruction are invalid"
        return s
    for i in range(1,4):
        if validity_check_register(temp_lst[i]) == False:
            s = "Invalid registers"
            return s
    opcode_str = returnbin(instruction_code['and'],5)
    print_machine_code = opcode_str + "00" + returnbin(reg_bin[temp_lst[1]], 3) + returnbin(reg_bin[temp_lst[2]], 3) + returnbin(reg_bin[temp_lst[3]], 3)
    # print(print_machine_code)
    return print_machine_code

def invert_print(instruction):
    global instruction_code
    lst = instruction.split()
    if (validity_check_opcode(lst[0]) == False):
        s = "Invalid opcode"
        return s
    if len(lst) != 3:
        s = "Number of arguments in invert instruction are invalid"
        return s
    for i in range(1,3):
        if validity_check_register(lst[i]) == False:
            s = "Invalid register"
            return s
    dest_reg = reg_bin.get(lst[1])
    src_reg = reg_bin.get(lst[2])
    dest_reg_bin = returnbin(dest_reg, 3)
    src_reg_bin = returnbin(src_reg, 3)
    print_machine_code = returnbin(instruction_code['not'], 5) + "00000" + dest_reg_bin + src_reg_bin
    # print(print_machine_code)
    return print_machine_code

def compare_print(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    if validity_check_opcode(templst[0]) == False:
        s = "Invalid opcode"
        return s
    if len(templst) != 3:
        s = "Number of arguments in compare instruction are invalid"
        return s
    j = 1
    for i in range(2):
        if validity_check_register(templst[j]) == False:
            s = "Invalid register"
            return s
        j += 1
    opcodestr = returnbin(instruction_code['cmp'],5)
    #print_machine_code = print_machine_code  + "00" + returnbin(reg_lst(templst[1]),3)+ returnbin(reg_lst(templst[2]),3)+ returnbin(reg_lst(templst[3]),3)
    print_machine_code = opcodestr + "00000" + returnbin(reg_bin[templst[1]],3)+returnbin(reg_bin[templst[2]],3)
    # print(print_machine_code)
    return print_machine_code

def unconditional_jump(instruction):
    global instruction_code
    lst = instruction.split()
    # assert len(lst) == 2, "number of arguments in instruction is invalid"
    if len(lst) != 2:
        s = "Number of arguments in unconditional jump instruction is invalid"
        return s
    # assert validity_check_opcode(lst[0]) == True, "Invalid instruction"
    if validity_check_opcode(lst[0]) == False:
        s = "Invalid opcode"
        return s
    # assert validity_check_mem_address(lst[1]) == True, "Invalid memory address"
    if lst[1] not in label_dict:
        s = "Label not found"
        return s
    print_machine_code = returnbin(instruction_code['jmp'],5) + "0000" + returnbin(label_dict[lst[1]], 7)
    # print(print_machine_code)
    return print_machine_code

def jlt_print(instruction):
    global instruction_code
    temp_lst = instruction.split()
    # assert len(temp_lst) == 2, "number of arguments in load instruction is invalid"
    if len(temp_lst) != 2:
        s = "Number of arguments in jump if less than instruction are invalid"
        return s
    # assert validity_check_opcode(temp_lst[0]) == True, "Invalid instruction"
    if validity_check_opcode(temp_lst[0]) == False:
        s = "Invalid opcode"
        return s
    # assert validity_check_mem_address(temp_lst[1]) == True, "Invalid memory address"
    if temp_lst[1] not in label_dict:
        s = "Label not found"
        return s
    opcode_str = returnbin(instruction_code['jlt'],5)
    print_machine_code = opcode_str + "0000" + returnbin(label_dict[temp_lst[1]], 7)
    # print(print_machine_code)
    return print_machine_code

def jgt_print(instruction):
    global instruction_code
    # Checking validity
    templst = instruction.split()
    # assert validity_check_opcode(templst[0]) == True, "invalid opcode"
    if validity_check_opcode(templst[0]) == False:
        s = "Invalid opcode"
        return s
    # assert len(templst) == 2, "number of args in jump if equal instruction is invalid"
    if len(templst) != 2:
        s = "number of arguments in jump if equal instruction are invalid"
        return s
    mem_addr = templst[1]
    # assert validity_check_mem_address(mem_addr) == True, "invalid memory address"
    if templst[1] not in label_dict:
        s = "Label not found"
        return s
    opcodestr = returnbin(instruction_code['jgt'], 5)
    print_machine_code = opcodestr + "0000" + returnbin(label_dict[templst[1]], 7)
    # print(print_machine_code)
    return print_machine_code

def je_print(instruction):
    global instruction_code
    # Checking validity
    templst = instruction.split()
    # assert validity_check_opcode(templst[0]) == True, "invalid opcode"
    if validity_check_opcode(templst[0]) == False:
        s = "Invalid opcode"
        return s
    # assert len(templst) == 2, "number of args in jump if equal instruction is invalid"
    if len(templst) != 2:
        s = "Number of arguments in jump if equal instruction are invalid"
        return s
    mem_addr = templst[1]
    # assert validity_check_mem_address(mem_addr) == True, "invalid memory address"
    if templst[1] not in label_dict:
        s = "Label not found"
        return s
    opcodestr = returnbin(instruction_code['je'], 5)
    print_machine_code = opcodestr + "0000" + returnbin(label_dict[templst[1]], 7)
    # print(print_machine_code)
    return print_machine_code

def halt_print(instruction):
    instruction = instruction.strip()
    global instruction_code
    # Checking validity
    # assert validity_check_opcode(instruction) == True, "invalid opcode"
    if validity_check_opcode(instruction) == False:
        print("reached")
        s = "Invalid opcode"
        return s
    # assert len(instruction.split()) == 1, "number of args in halt instruction is invalid"
    if len(instruction.split()) != 1:
            s = "Number of arguments in halt instruction are invalid"
            return s
    opcodestr = returnbin(instruction_code['hlt'], 5)
    print_machine_code = opcodestr + "00000000000"
    # print(print_machine_code)
    return print_machine_code

def addf_print(instruction):
    global instruction_code
    #checking validity
    temp_lst = instruction.split()
    if validity_check_opcode(temp_lst[0]) == False:
        s = "Invalid opcode"
        return s
    if len(temp_lst) != 4:
        s = "Number of arguments in additionf instruction are invalid"
        return s
    for i in range(1,4):
        if validity_check_register(temp_lst[i]) == False:
            s = "Invalid registers"
            return s
    opcode_str = returnbin(instruction_code['addf'],5)
    print_machine_code = opcode_str + "00" + returnbin(reg_bin[temp_lst[1]], 3) + returnbin(reg_bin[temp_lst[2]], 3) + returnbin(reg_bin[temp_lst[3]], 3)
    # print(print_machine_code)
    return print_machine_code

def subf_print(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    if validity_check_opcode(templst[0]) == False:
        s = "Invalid opcode"
        return s
    if len(templst) != 4:
        s = "Number of arguments in subtraction instruction are invalid"
        return s
    j = 1
    for i in range(3):
        if validity_check_register(templst[j]) == False:
            s = "Invalid register"
            return s
        j += 1
    opcodestr = returnbin(instruction_code['subf'],5)
    # print_machine_code = print_machine_code  + "00" + returnbin(reg_lst(templst[1]),3)+ returnbin(reg_lst(templst[2]),3)+ returnbin(reg_lst(templst[3]),3)
    print_machine_code = opcodestr + "00" + returnbin(reg_bin[templst[1]],3)+returnbin(reg_bin[templst[2]],3)+returnbin(reg_bin[templst[3]],3)
    # print(print_machine_code)
    return print_machine_code

def movef_immediate(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    if validity_check_opcode(templst[0]) == False:
        s = "Invalid opcode"
        return s
    if len(templst) != 3:
        s = "Number of arguments in move_immediate instruction are invalid"
        return s
    if validity_check_register(templst[1]) == False:
        s = "Invalid register"
        return s
    imm = templst[2]
    imm = imm[1:]
    imm = int(imm)
    if imm < 0 or imm > 127:
        s = "Immediate value out of range"
        return s
    opcodestr = returnbin(instruction_code['movf_imm'], 5)
    print_machine_code = opcodestr + returnbin(reg_bin[templst[1]], 3) + returnbin(imm, 8)
    # print(print_machine_code)
    return print_machine_code


# reading input from test.txt
# with open("assembly_code.txt",'r') as f:
#     lines = f.read()

lines = sys.stdin.read()
lines = lines.split('\n')
while '' in lines:
    lines.remove('')

halt = True
inscount = 0
varcount = 0

var_ok = True

for line in lines:
    if line[:3] == "var":
        varcount+=1
    else:
        inscount += 1

for i in range(varcount):
    vardictionary[lines[i][4:]] = i+inscount

for i in range(inscount):
    l = lines[i+varcount]
    if l[:3] == "var":
        var_ok = False
    if ":" in l:
        temp = l.split()
        label_dict[temp[0][:-1]] = i    
        insdict[i] = " ".join(temp[1:])
    else:
        insdict[i] = l

if list(insdict.values())[-1] != "hlt":
    halt = False

#fout = open("machine_code.txt",'w')
fout = sys.stdout
for line in insdict.values():
    # print(line)
    ins = line
    newins = ""
    temp = line.split()

    if not var_ok:
        fout.write("variables not all declared in the beginning\n")
        break
    
    if not halt:
        fout.write("Halt found in the middle of instructions, program terminated\n")
        break
    command = temp[0]

    if 'FLAGS' in temp and (command != 'mov' or temp.index('FLAGS') == 1):
        fout.write("Invalid Usage of Flags with instruction other than move\n")
        break


    if command == 'add':
        s = add_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'sub':
        s = sub_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'mov':
        if '$' in ins:
            ins = ins.replace('mov', 'mov_imm')
            s  = move_immediate(ins)
            s += '\n'
            fout.write(s)
        else:
            ins = ins.replace('mov','mov_reg')
            s = move_register(ins)
            s += '\n'
            fout.write(s)
    elif command == 'ld':
        s = ld_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'st':
        s = st_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'mul':
        s = mul_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'div':
        s = divide(ins)
        s += '\n'
        fout.write(s)
    elif command == 'rs':
        s = rs_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'xor':
        s = xor_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'or':
        s = or_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'and':
        s = and_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'not':
        s = invert_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'cmp':
        s = compare_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'jmp':
        s = unconditional_jump(ins)
        s += '\n'
        fout.write(s)
    elif command == 'jlt':
        s = jlt_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'jgt':
        s = jgt_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'je':
        s = je_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'addf':
        s= addf_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'subf':
        s= subf_print(ins)
        s += '\n'
        fout.write(s)
    elif command == 'movf':
        s= movef_immediate(ins)
        s += '\n'
        fout.write(s)
    elif command == 'hlt':
        s = halt_print(ins)
        s += '\n'
        fout.write(s)
fout.close()