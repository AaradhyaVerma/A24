opcodes = {"add": "00000", "sub": "00001", "mov1": "00010", "mov2": "00011", "ld": "00100", "st": "00101", "mul": "00110", "div": "00111", "rs": "01000", "ls": "01001",
           "xor": "01010", "or": "01011", "and": "01100", "not": "01101", "cmp": "01110", "jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111", "hlt": "11010"}
regs = {"R0": "000", "R1": "001", "R2": "010", "R3": "011",
        "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
stmtTypes = {"add": "A", "sub": "A", "mov1": "B", "mov2": "C", "ld": "D", "st": "D", "mul": "A", "div": "C", "rs": "B",
             "ls": "B", "xor": "A", "or": "A", "and": "A", "not": "C", "cmp": "C", "jmp": "E", "jlt": "E", "jgt": "E", "je": "E", "hlt": "F"}
unusedSpace = {"A": "00", "B": "", "C": "00000",
               "D": "", "E": "0000", "F": "00000000000"}
labellist=[]
t=8
file=open('test.txt','r')
lines=file.readlines()
lines = [line.rstrip('\n') for line in lines]
for elemen in lines:
    sp=elemen.split()
    if ':' in sp[0]:
        labellist.append(sp[0][:-1])
        labellist.append(((bin(t))[2:]).zfill(7))
        t=t+1
x=bool(0)
lst=[]
varlist=[]
errorlist=[]
varcheck=0
hltcheck=0
line=0
n=len(lines)
for i in range (0,n):
    a=input()
    l=[item.strip() for item in a.split()]

    if l==[]:
        line+=1
        continue
    else:
        if ':' in l[0]:
            l.pop(0)
        if hltcheck==0:
            if l[0]=='var' and varcheck==0:
                line+=1
                varlist.append(l[1])
                varlist.append(((bin(t))[2:]).zfill(7))
                t=t+1
            elif l[0]=='var' and varcheck!=0:
                line+=1
                err='error in line '+str(line)+' : variable must be declared at the beginning '
                errorlist.append(err)
            else:
                line+=1
                varcheck+=1
                if l[0] not in stmtTypes:
                    err='error in line '+str(line)+' : invalid operand'
                    errorlist.append(err)
                else:
                    check=stmtTypes[l[0]]
                    if check=='A':
                        if len(l)!=4:
                            err='error in line '+str(line)+' :this operand needs exactly 3 registers'
                            errorlist.append(err)
                        elif (l[1] not in regs) or (l[2] not in regs) or (l[3] not in regs):
                            err = 'error in line ' +str(line)+ ' : invalid register'
                            errorlist.append(err)
                        else:
                            bin1=opcodes[l[0]]
                            bin2=unusedSpace['A']
                            bin3=regs[l[1]]
                            bin4=regs[l[2]]
                            bin5=regs[l[3]]
                            s=bin1+bin2+bin3+bin4+bin5
                            lst.append(s)

                    elif check=='B':
                        if len(l)!=3:
                            err = 'error in line ' +str(line)+ ' :this operand only takes one register and one value'
                            errorlist.append(err)
                        elif l[1] not in regs:
                            err = 'error in line ' +str(line)+ ' :invalid register'
                            errorlist.append(err)
                        elif l[2][1:].isalpha():
                            err = 'error in line ' +str(line)+ ' :value is not integer'
                            errorlist.append(err)
                        else:
                            bin1=opcodes[l[0]]
                            bin3=regs[l[1]]
                            d=int(l[2][1:])
                            bin4=((bin(d))[2:]).zfill(8)
                            s=bin1+bin3+bin4
                            lst.append(s)
                    elif check=='C':
                        if len(l)!=3:
                            err = 'error in line ' +str(line)+ ' :this operand takes exactly 2 registers'
                            errorlist.append(err)
                        elif (l[1] not in regs) or (l[2] not in regs):
                            err = 'error in line ' +str(line)+ ' :invalid register'
                            errorlist.append(err)
                        else:
                            bin1 = opcodes[l[0]]
                            bin2 = unusedSpace['C']
                            bin3 = regs[l[1]]
                            bin4 = regs[l[2]]
                            s = bin1 + bin2 + bin3 + bin4
                            lst.append(s)
                    elif check=='D':
                        if len(l)!=3:
                            err = 'error in line ' +str(line)+ ' :this operand only takes one register and one memory address'
                            errorlist.append(err)
                        elif l[1] not in regs:
                            err = 'error in line ' +str(line)+ ' :invalid register'
                            errorlist.append(err)
                        elif l[2] not in varlist:
                            err = 'error in line ' +str(line)+ ' :invalid variable(not defined)'
                            errorlist.append(err)
                        else:
                            bin1=opcodes[l[0]]
                            bin2=unusedSpace['D']
                            bin3=regs[l[1]]
                            bin4=varlist[(varlist.index(l[2]))+1]
                            s=bin1+bin2+bin3+bin4
                            lst.append(s)
                    elif check=='E':
                        if len(l)!=2:
                            err = 'error in line ' +str(line)+ ' :this operand only takes one memory address'
                            errorlist.append(err)
                        elif l[1] not in labellist:
                            err='error in line '+str(line)+ ' :this label is not defined'
                            errorlist.append(err)
                        else:
                            bin1=opcodes[l[0]]
                            bin2=unusedSpace['E']
                            bin3=labellist[(labellist.index(l[1]))+1]
                            s=bin1+bin2+bin3
                            lst.append(s)
                    elif check=='F':
                        if len(l)!=1:
                            err = 'error in line ' +str(line)+ ' :there should be no keyword after hlt'
                            errorlist.append(err)
                        else:
                            bin1=opcodes[l[0]]
                            bin2=unusedSpace['F']
                            s=bin1+bin2
                            lst.append(s)
                            x=bool(1)
                            hltcheck+=1
        else:
            err='error in line: '+str(line+1)+' :commands after hlt operand are invalid'
            errorlist.append(err)
if l[0]!='hlt':
    err='error in line '+str(line)+' :no hlt operand at the end'
    errorlist.append(err)
if errorlist==[]:
    for elm in lst:
        print(elm)
else:
    for elm in errorlist:
        if 'commands after hlt operand are invalid' not in elm:
            print(elm)
        else:
            print(elm)
            break
