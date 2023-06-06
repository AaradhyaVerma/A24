from assembler import *
def validity_check_mem_address(mem_addr):
    global mem_bin
    if mem_addr in mem_bin:
        return True
    else:
        return False

def validity_check_imm(immediate):
    immediate = immediate[1:]
    if 0 <= int(immediate) <= 127:
        return True
    return False

def st_print(instruction):
    temp_lst = instruction.split()
    assert len(temp_lst) == 3, "number of arguments in load instruction is invalid"
    assert validity_check_opcode(temp_lst[0]) == True, "instruction is invalid"
    assert validity_check_register(temp_lst[1]) == True, "register is invalid"
    opcode_str = returnbin(instruction_code['st'],5)
    print_machine_code = opcode_str + "0" + returnbin(reg_bin[temp_lst[1]], 3) + returnbin(mem_bin[temp_lst[2]], 7)
    print(print_machine_code)

def ls_print(instruction):
    global instruction_code 
    #checking validity
    templst = instruction.split()
    assert validity_check_opcode(templst[0]) == True, "invalid opcode"
    assert len(templst) == 3, "number of args in move imm instruction is invalid"
    assert validity_check_register(templst[1]) == True, "invalid register"
    imm=templst[2]
    imm = imm[1:]
    imm = int(imm)
    opcode_str = returnbin(instruction_code['ls'],5)
    print_machine_code = opcode_str + "0" + returnbin(reg_bin[templst[1]], 3) + returnbin(imm,7)
    print(print_machine_code)
ls_print("ls R1 $28")
def invert_print(instruction):
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
    final_inst = returnbin(instruction_code['not'], 5) + "00000" + dest_reg_bin + src_reg_bin
    print(final_inst)

def jgt_print(instruction):
    global instruction_code
    # Checking validity
    templst = instruction.split()
    assert validity_check_opcode(templst[0]) == True, "invalid opcode"
    assert len(templst) == 2, "number of args in jump if equal instruction is invalid"
    mem_addr = templst[1]
    assert validity_check_mem_address(mem_addr) == True, "invalid memory address"
    opcodestr = returnbin(instruction_code['jgt'], 5)
    printable = opcodestr + "0000" + returnbin(mem_bin[templst[1]], 7)
    print(printable)