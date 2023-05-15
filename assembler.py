
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

#creating dicts for opcodes

