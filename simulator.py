import sys
R0 = R1 = R2 = R3 = R4 = R5 = R6 = FLAGS = "0000000000000000"

reg_type = {
    "000": R0,
    "001": R1,
    "010": R2,
    "011": R3,
    "100": R4,
    "101": R5,
    "110": R6,
    "111": FLAGS
}

inst_type={"A":["00000","00001","00110","01010","01011","01100","10000","10001"],
           "B":["00010","01000","01001","10010"],
           "C":["00011","00111","01101","01110"],
           "D":["00100","00101"],
           "E":["01111","11100","11101","11111"],
           "F":["11010"]}

MEM=["0000000000000000"]*128

def decimal_to_binary(num,bits):
    s = bin(num)
    s = s[2:] 
    assert(len(s) <= bits),"number cannot be represented in given number of bits"
    for i in range(bits - len(s)):
        s = '0' + s
    return s


def binary_to_decimal(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal * 2 + int(digit)
    return decimal
    

def ieee_to_decimal(ie):
    ie = str(ie)
    exp_bin = ie[:3]
    exp = int(exp_bin, 2)
    wh_bin = "1" + ie[3:exp+3].ljust(exp+1, '0')
    bin = ie[exp+3:]
    dec = int(wh_bin + bin, 2)
    return dec

def decimal_to_ieee(n):
    global checker
    n = float(n)
    wh = int(n)
    len_bin = len(str(bin(wh)[2:]))
    if (len_bin>8):
        checker=1
    else: 
        dec = float(n-wh)
        bin_wh = bin(wh)[2:]
        bi = str(bin_wh) + str(decimal_to_binary(dec))
        exp = bin(len(str(bin(wh)[2:]))-1)[2:]
        exp = "0"*(3-len(exp))+exp
        ans = str(exp) + bi[1:]
        ans = ans[:8]
        if (ieee_to_decimal(ans)!=n):
            checker=1
        return ans


sim_inst=sys.stdin.read()
lines=sim_inst.split("\n")
if(lines[-1]==''):
    lines=lines[:-1]

p=0
  
def initialize():
    global p
    for i in lines:
        op = i[:5]
        t = [op]
        if op in inst_type["A"]:
            t.append(i[5:7])
            t.append(i[7:10])
            t.append(i[10:13])
            t.append(i[13:16])
        elif op in inst_type["B"]:
            t.append(i[5:8])
            t.append(i[8:16])
        elif op in inst_type["C"]:
            t.append(i[5:10])
            t.append(i[10:13])
            t.append(i[13:16])
        elif op in inst_type["D"]:
            t.append(i[5:8])
            t.append(i[8:16])
        elif op in inst_type["E"]:
            t.append(i[5:8])
            t.append(i[8:16])
        elif op in inst_type["F"]:
            t.append(i[5:16])
        MEM[p] = t
        p += 1

program_counter=0
halted=False

orv=0

def execute(instruction,x,y,cycle):
    global program_counter
    global halted
    global checker
    global orv
    op=instruction[0]
    if op==inst_type["A"][0]:
        reg_type[instruction[4]]=reg_type[instruction[2]]+reg_type[instruction[3]]
        if (reg_type[instruction[4]]>16384 or reg_type[instruction[4]]<0):
            reg_type["111"]=8
            reg_type[instruction[4]]=reg_type[instruction[4]]%16384
            orv=1
        program_counter+=1

    if op==inst_type["A"][1]:
        reg_type[instruction[4]]=reg_type[instruction[2]]-reg_type[instruction[3]]
        if (reg_type[instruction[4]]>16384 or reg_type[instruction[4]]<0):
            reg_type["111"]=8
            reg_type[instruction[4]]=reg_type[instruction[4]]%16384
            orv=1
        program_counter+=1

    if op==inst_type["A"][2]:
        reg_type[instruction[4]]=reg_type[instruction[2]]*reg_type[instruction[3]]
        if (reg_type[instruction[4]]>16384 or reg_type[instruction[4]]<0):
            reg_type["111"]=8
            reg_type[instruction[4]]=reg_type[instruction[4]]%16384
            orv=1
        program_counter+=1
    if op==inst_type["A"][3]:
        reg_type[instruction[4]]=reg_type[instruction[2]]^reg_type[instruction[3]]
        program_counter+=1
    
    if op==inst_type["A"][4]:
        reg_type[instruction[4]]=reg_type[instruction[2]]|reg_type[instruction[3]]
        program_counter+=1

    if op==inst_type["A"][5]:
        reg_type[instruction[4]]=reg_type[instruction[2]]&reg_type[instruction[3]]
        program_counter+=1

    if op==inst_type["A"][6]:
        reg_type[instruction[4]]=reg_type[instruction[2]]+reg_type[instruction[3]]
        decimal_to_ieee(reg_type[instruction[4]])
        if(checker==1):
            reg_type["111"]=8
            reg_type[instruction[4]]=128.0
            checker=0
            orv=1
        program_counter+=1

    if op==inst_type["A"][7]:
        reg_type[instruction[4]]=reg_type[instruction[2]]-reg_type[instruction[3]]
        decimal_to_ieee(reg_type[instruction[4]])
        if(checker==1):
            reg_type["111"]=8
            reg_type[instruction[4]]=0
            checker=0
            orv=1
        program_counter+=1
                
    if op==inst_type["B"][0]:
        reg_type[instruction[1]]=binary_to_decimal(instruction[2])
        program_counter+=1
    
    if op==inst_type["B"][1]:
        reg_type[instruction[1]]=reg_type[instruction[1]]>>binary_to_decimal(instruction[2])
        program_counter+=1
    
    if op==inst_type["B"][2]:
        reg_type[instruction[1]]=reg_type[instruction[1]]<<binary_to_decimal(instruction[2])
        program_counter+=1

    if op==inst_type["C"][0]:
        reg_type[instruction[3]]=reg_type[instruction[2]]
        program_counter+=1

    if op==inst_type["B"][3]:
        reg_type[instruction[1]]=ieee_to_decimal(instruction[2])
        pc_temp+=1

    if op==inst_type["C"][1]:
        reg_type["000"]=reg_type[instruction[2]]//reg_type[instruction[3]]
        reg_type["001"]=reg_type[instruction[2]]%reg_type[instruction[3]]
        program_counter+=1

    if op==inst_type["C"][2]:
        reg_type[instruction[3]]=~reg_type[instruction[2]]
        program_counter+=1

    if op==inst_type["C"][3]:
        if(reg_type[instruction[2]]<reg_type[instruction[3]]):
            reg_type["111"]=4
        if(reg_type[instruction[2]]>reg_type[instruction[3]]):
            reg_type["111"]=2
        if(reg_type[instruction[2]]==reg_type[instruction[3]]):
            reg_type["111"]=1
        program_counter+=1
        orv=1

    if op==inst_type["D"][0]:
        x.append(cycle)
        y.append(binary_to_decimal(instruction[2]))
        reg_type[instruction[1]]=binary_to_decimal(MEM[binary_to_decimal(instruction[2])])
        program_counter+=1

    
    if op==inst_type["D"][1]:
        x.append(cycle)
        y.append(binary_to_decimal(instruction[2]))
        t=decimal_to_binary(reg_type[instruction[1]])
        a=16-len(t)
        MEM[binary_to_decimal(instruction[2])]='0'*a+t
        program_counter+=1

    if op==inst_type["E"][0]:
        program_counter=binary_to_decimal(instruction[2])
        


    if op==inst_type["E"][1]:
        if reg_type["111"]==4:
            program_counter=binary_to_decimal(instruction[2])
        else:
            program_counter+=1
        
    
    if op==inst_type["E"][2]:
        if reg_type["111"]==2:
            program_counter=binary_to_decimal(instruction[2])
        else:
            program_counter+=1
        
    
    if op==inst_type["E"][3]:
        if reg_type["111"]==1:
            program_counter=binary_to_decimal(instruction[2])
        else:
            program_counter+=1

    if op==inst_type["F"][0]:
        halted=True

    if(orv==0):
        reg_type["111"]=0
    orv=0

    return halted,program_counter


initialize()
pc=0

x=[]
y=[]
cycle=0


while(not halted):
    x.append(cycle)
    y.append(pc)
    Instruction=MEM[pc]
    halted,new_pc=execute(Instruction,x,y,cycle)
    t=decimal_to_binary(pc)
    a=8-len(t)
    s='0'*a+t
    sys.stdout.write(s+' ')
    print(s,end=" ")
    for i in reg_type:
        if(type(reg_type[i])==float):
            t=decimal_to_ieee(reg_type[i])
        else:
            t=decimal_to_binary(reg_type[i])
        a=16-len(t)
        s='0'*a+t
        sys.stdout.write(s+' ')
        print(s,end=" ")
    sys.stdout.write("\n")
    pc=new_pc
    cycle+=1

for i in MEM:
    
    if type(i)==list:
        s=''.join(i)
        sys.stdout.write(s+'\n')
    else:
        sys.stdout.write(i+'\n')

#bonus square, ones complement, double addition, LCM, HCF, 