reg_bin = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6}


#creating a decimal to binary converter which takes the decimal and the number of bits as input
def returnbin(num,bits):
    s = bin(num)
    s = s[2:] 
    assert(len(s) < bits),"number cannot be represented in given number of bits"
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
         'jlt':16,
         'jgt':17,
         'je':18,
         'hlt':19}

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

def sub_print(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    assert len(templst) == 4, "number of args in subtract instruction is invalid"
    opcodestr = returnbin(instruction_code['sub'],5)
    #printable = printable  + "00" + returnbin(reg_lst(templst[1]),3)+ returnbin(reg_lst(templst[2]),3)+ returnbin(reg_lst(templst[3]),3)
    printable = opcodestr + "00" + returnbin(reg_bin[templst[1]],3)+returnbin(reg_bin[templst[2]],3)+returnbin(reg_bin[templst[3]],3)
    print(printable)