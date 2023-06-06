minelt = 10000
stack = [3,4,6,7,2]
def popmin():
    global stack
    global minelt
    if(len(stack) == 0):
        return
    x = stack.pop()
    minelt = min(minelt,x)
    popmin()
    print(minelt)
    if(x != minelt):
        templst = []
        templst.append(x)
        stack = stack + templst
popmin()
print(stack)
