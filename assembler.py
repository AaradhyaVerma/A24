reg_bin = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6}


#creating a decimal to binary converter which takes the decimal and the number of bits as input
def returnbin(num,bits):
    s = bin(num)
    s = s[2:]
    if(len(s) > bits):
        print("number cannot be represented in given number of bits")
        return
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

