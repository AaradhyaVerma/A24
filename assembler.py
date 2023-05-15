reg_bin = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6}
mem_bin = {"label0": 0, "label1": 1, "label2": 2, "label3": 3, "label4": 4, "label5": 5, "label6": 6}

#creating a decimal to binary converter which takes the decimal and the number of bits as input
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
         'hlt':26}

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
         'hlt':"F"}

var_dict = {}
#function for inserting vars in dict which takes line number, name as input
def insert_var_in_dict(name,line_num):
    global var_dict
    var_dict[name] = returnbin(line_num,16)

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
    assert (validity_check_opcode(temp_lst[0]) == True), "Invalid instruction"
    assert len(temp_lst) == 4, "number of arguments in addition instruction is invalid"
    for i in range(1,4):
        assert validity_check_register(temp_lst[i]) == True, "format of registers is invalid"
    opcode_str = returnbin(instruction_code['add'],5)
    print_machine_code = opcode_str + "00" + returnbin(reg_bin[temp_lst[1]], 3) + returnbin(reg_bin[temp_lst[2]], 3) + returnbin(reg_bin[temp_lst[3]], 3)
    print(print_machine_code)

def sub_print(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    assert validity_check_opcode(templst[0]) == True, "invalid opcode"
    assert len(templst) == 4, "number of args in subtract instruction is invalid"
    j = 1
    for i in range(3):
        assert validity_check_register(templst[j]) == True, "invalid register"
        j+=1
    opcodestr = returnbin(instruction_code['sub'],5)
    #printable = printable  + "00" + returnbin(reg_lst(templst[1]),3)+ returnbin(reg_lst(templst[2]),3)+ returnbin(reg_lst(templst[3]),3)
    printable = opcodestr + "00" + returnbin(reg_bin[templst[1]],3)+returnbin(reg_bin[templst[2]],3)+returnbin(reg_bin[templst[3]],3)
    print(printable)

def move_immediate(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    assert validity_check_opcode(templst[0]) == True, "invalid opcode"
    assert len(templst) == 3, "number of args in move imm instruction is invalid"
    assert validity_check_register(templst[1]) == True, "invalid register"
    imm=templst[2]
    imm = imm[1:]
    imm = int(imm)
    assert imm >= 0 and imm <= 127, "Immediate value out of range"
    opcodestr = returnbin(instruction_code['mov_imm'], 5)
    printable = opcodestr +"0"+ returnbin(reg_bin[templst[1]], 3) + returnbin(imm, 7)
    print(printable)

def move_register(instruction):
    global instruction_code
    lst = instruction.split()
    assert (validity_check_opcode(lst[0]) == True), "Invalid instruction"
    assert len(lst) == 3, "number of arguments in move registers instruction is invalid"
    for i in range(1,3):
        assert validity_check_register(lst[i]) == True, "format of registers is invalid"
    dest_reg = reg_bin.get(lst[1])
    src_reg = reg_bin.get(lst[2])
    dest_reg_bin = returnbin(dest_reg, 3)
    src_reg_bin = returnbin(src_reg, 3)
    final_inst = returnbin(instruction_code['mov_reg'], 5) + "00000" + dest_reg_bin + src_reg_bin
    print(final_inst)

def ld_print(instruction):
    global instruction_code
    temp_lst = instruction.split()
    assert len(temp_lst) == 3, "number of arguments in load instruction is invalid"
    assert validity_check_opcode(temp_lst[0]) == True, "instruction is invalid"
    assert validity_check_register(temp_lst[1]) == True, "register is invalid"
    assert validity_check_mem_address(temp_lst[2]) == True, "memory address is invalid"
    opcode_str = returnbin(instruction_code['ld'],5)
    print_machine_code = opcode_str + "0" + returnbin(reg_bin[temp_lst[1]], 3) + returnbin(mem_bin[temp_lst[2]], 7)
    print(print_machine_code)

def mul_print(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    assert validity_check_opcode(templst[0]) == True, "invalid opcode"
    assert len(templst) == 4, "number of args in multiply instruction is invalid"
    j = 1
    for i in range(3):
        assert validity_check_register(templst[j]) == True, "invalid register"
        j+=1
    opcodestr = returnbin(instruction_code['mul'],5)
    #printable = printable  + "00" + returnbin(reg_lst(templst[1]),3)+ returnbin(reg_lst(templst[2]),3)+ returnbin(reg_lst(templst[3]),3)
    printable = opcodestr + "00" + returnbin(reg_bin[templst[1]],3)+returnbin(reg_bin[templst[2]],3)+returnbin(reg_bin[templst[3]],3)
    print(printable)

def divide(instruction):
    global instruction_code
    lst = instruction.split()
    assert (validity_check_opcode(lst[0]) == True), "Invalid instruction"
    assert len(lst) == 3, "number of arguments in division instruction is invalid"
    for i in range(1,3):
        assert validity_check_register(lst[i]) == True, "format of registers is invalid"
    dest_reg = reg_bin.get(lst[1])
    src_reg = reg_bin.get(lst[2])
    dest_reg_bin = returnbin(dest_reg, 3)
    src_reg_bin = returnbin(src_reg, 3)
    final_inst = returnbin(instruction_code['div'], 5) + "00000" + dest_reg_bin + src_reg_bin
    print(final_inst)

def xor_print(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    assert validity_check_opcode(templst[0]) == True, "invalid opcode"
    assert len(templst) == 4, "number of args in XOR instruction is invalid"
    j = 1
    for i in range(3):
        assert validity_check_register(templst[j]) == True, "invalid register"
        j+=1
    opcodestr = returnbin(instruction_code['xor'],5)
    #printable = printable  + "00" + returnbin(reg_lst(templst[1]),3)+ returnbin(reg_lst(templst[2]),3)+ returnbin(reg_lst(templst[3]),3)
    printable = opcodestr + "00" + returnbin(reg_bin[templst[1]],3)+returnbin(reg_bin[templst[2]],3)+returnbin(reg_bin[templst[3]],3)
    print(printable)

def Or(instruction):
    global instruction_code
    lst = instruction.split()
    assert (validity_check_opcode(lst[0]) == True), "Invalid instruction"
    assert len(lst) == 4, "number of arguments in or instruction is invalid"
    for i in range(1,4):
        assert validity_check_register(lst[i]) == True, "format of registers is invalid"

    dest_reg = reg_bin.get(lst[1])
    src_reg1 = reg_bin.get(lst[2])
    src_reg2 = reg_bin.get(lst[3])

    dest_reg_bin = returnbin(dest_reg, 3)
    src_reg1_bin = returnbin(src_reg1, 3)
    src_reg2_bin = returnbin(src_reg2, 3)

    final_inst = returnbin(instruction_code['or'], 5) + "00" + dest_reg_bin + src_reg1_bin + src_reg2_bin
    print(final_inst)

def and_print(instruction):
    global instruction_code
    #checking validity
    temp_lst = instruction.split()
    assert (validity_check_opcode(temp_lst[0]) == True), "Invalid instruction"
    assert len(temp_lst) == 4, "number of arguments in logical-and instruction is invalid"
    for i in range(1,4):
        assert validity_check_register(temp_lst[i]) == True, "format of registers is invalid"
    opcode_str = returnbin(instruction_code['and'],5)
    print_machine_code = opcode_str + "00" + returnbin(reg_bin[temp_lst[1]], 3) + returnbin(reg_bin[temp_lst[2]], 3) + returnbin(reg_bin[temp_lst[3]], 3)
    print(print_machine_code)

def compare_print(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    assert validity_check_opcode(templst[0]) == True, "invalid opcode"
    assert len(templst) == 3, "number of args in compare instruction is invalid"
    j = 1
    for i in range(2):
        assert validity_check_register(templst[j]) == True, "invalid register"
        j+=1
    opcodestr = returnbin(instruction_code['cmp'],5)
    #printable = printable  + "00" + returnbin(reg_lst(templst[1]),3)+ returnbin(reg_lst(templst[2]),3)+ returnbin(reg_lst(templst[3]),3)
    printable = opcodestr + "00000" + returnbin(reg_bin[templst[1]],3)+returnbin(reg_bin[templst[2]],3)
    print(printable)

def unconditional_jump(instruction):
    global instruction_code
    lst = instruction.split()
    assert len(lst) == 2, "number of arguments in instruction is invalid"
    assert validity_check_opcode(lst[0]) == True, "Invalid instruction"
    assert validity_check_mem_address(lst[1]) == True, "Invalid memory address"
    final_inst = returnbin(instruction_code['jmp'],5) + "0000" + returnbin(mem_bin[lst[1]], 7)
    print(final_inst)

def je_print(instruction):
    global instruction_code
    # Checking validity
    templst = instruction.split()
    assert validity_check_opcode(templst[0]) == True, "invalid opcode"
    assert len(templst) == 2, "number of args in jump if equal instruction is invalid"
    mem_addr = templst[1]
    assert validity_check_mem_address(mem_addr) == True, "invalid memory address"
    opcodestr = returnbin(instruction_code['je'], 5)
    printable = opcodestr + "0000" + returnbin(mem_bin[templst[1]], 7)
    print(printable)

def jlt_print(instruction):
    global instruction_code
    temp_lst = instruction.split()
    assert len(temp_lst) == 2, "number of arguments in load instruction is invalid"
    assert validity_check_opcode(temp_lst[0]) == True, "Invalid instruction"
    assert validity_check_mem_address(temp_lst[1]) == True, "Invalid memory address"
    opcode_str = returnbin(instruction_code['jlt'],5)
    print_machine_code = opcode_str + "0000" + returnbin(mem_bin[temp_lst[1]], 7)
    print(print_machine_code)

def rs_print(instruction):
    global instruction_code
    temp_lst = instruction.split()
    temp_lst[2] = temp_lst[2][1:]
    assert len(temp_lst) == 3, "number of arguments in load instruction is invalid"
    assert validity_check_opcode(temp_lst[0]) == True, "Invalid instruction code"
    assert validity_check_register(temp_lst[1]) == True, "Invalid register"
    # assert validity_check_imm(temp_lst[2]) == True, "Invalid immediate"
    imm = int(temp_lst[2])
    assert imm >= 0 and imm <= 127, "Immediate value out of range"
    opcode_str = returnbin(instruction_code['rs'],5)
    print_machine_code = opcode_str + "0" + returnbin(reg_bin[temp_lst[1]], 3) + returnbin(imm, 7)
    print(print_machine_code)

def halt_print(instruction):
    global instruction_code
    # Checking validity
    assert validity_check_opcode(instruction) == True, "invalid opcode"
    assert len(instruction.split()) == 1, "number of args in halt instruction is invalid"
    opcodestr = returnbin(instruction_code['hlt'], 5)
    printable = opcodestr + "00000000000"
    print(printable)