import enigma
from enigma import *

# SEARCH FOR A CONTRADICTION (CRIB, CIPHERTEXT, LETTERED POSITION, 2 BYTE STRING)
def contradiction(inpt,output,pos,guess):
    n = len(inpt)
    leftover = [x for x in range(26)]
    leftover.remove(guess[0])
    if guess[0] != guess[1]:
        leftover.remove(guess[1])
    g = {x:'+' for x in leftover}
    g[guess[0]] = guess[1]
    g[guess[1]] = guess[0]
    line1 = inpt
    line2 = [g[x] for x in inpt]
    line3 = [g[x] for x in output]
    line4 = output
    line2old = []
    line3old = []
    while (line2 != line2old) | (line3 != line3old):
        line2old = line2
        line3old = line3
        for i in range(n):
            if (line2[i] == '+') & (line3[i] != '+'):
                missing = single(pos[i],line3[i])
                g[line1[i]] = missing
                g[missing] = line1[i]
                line2 = [g[x] for x in line1]
                line3 = [g[x] for x in line4]
            if (line3[i] == '+') & (line2[i] != '+'):
                missing = single(pos[i],line2[i])
                g[line4[i]] = missing
                g[missing] = line4[i]
                line2 = [g[x] for x in line1]
                line3 = [g[x] for x in line4]
    test = [single(pos[i],line2[i]) for i in range(n)]
    return( test == line3 )

# SEARCH FOR A CONTRADICTION (CRIB, CIPHERTEXT, LETTERED POSITION, 2 BYTE STRING)
def contradiction2(inpt,outpt,pos,guess):
    n=len(inpt)
    leftover = [x for x in range(26)]
    leftover.remove(guess[0])
    if guess[0] != guess[1]:
        leftover.remove(guess[1])
    g = {x:'+' for x in leftover}
    g[guess[0]] = guess[1]
    g[guess[1]] = guess[0]
    line1 = [x for x in inpt]
    line2 = [g[x] for x in inpt]
    line3 = [g[x] for x in outpt]
    line4 = [x for x in outpt]
    deduceup = []
    deducedown = []
    deduceboth = []
    left = [x for x in range(n)]
    for i in left:
        x = (g[line1[i]] != '+')
        y = (g[line4[i]] != '+')
        if x and not y:
            line2[i] = g[line1[i]]
            deducedown.append(i)
        elif y and not x:
            line3[i] = g[line4[i]]
            deduceup.append(i)
        elif x and y:
            line2[i] = g[line1[i]]
            line3[i] = g[line4[i]]
            deduceboth.append(i)
    flag = True
    while deduceboth + deducedown + deduceup != []:
        for i in deduceboth:
            if single(pos[i],line2[i]) == line3[i]:
                left.remove(i)
            else:
                flag = False
                break
        deduceboth = []
        if flag:
            for i in deduceup:
                x = single(pos[i],line3[i])
                if not ((g[line1[i]] in ['+',x]) and (g[x] in ['+',line1[i]])):
                    #if not (g[x] in ['+',line1[i]]):
                    flag = False
                    break
                g[x] = line1[i]
                g[line1[i]] = x
                line2[i] = x
                left.remove(i)
            for i in deducedown:
                x = single(pos[i],line2[i])
                if not ((g[line4[i]] in ['+',x]) and (g[x] in ['+',line4[i]])):
                    #if not (g[x] in ['+',line4[i]]):
                    flag = False
                    break
                g[x] = line4[i]
                g[line4[i]] = x
                line3[i] = x
                left.remove(i)
        deduceup = []
        deducedown = []
        if flag:
            for i in left:
                x = (g[line1[i]] != '+')
                y = (g[line4[i]] != '+')
                if x and not y:
                    line2[i] = g[line1[i]]
                    deducedown.append(i)
                elif y and not x:
                    line3[i] = g[line4[i]]
                    deduceup.append(i)
                elif x and y:
                    line2[i] = g[line1[i]]
                    line3[i] = g[line4[i]]
                    deduceboth.append(i)
    return(flag)

# SEARCH BY ROTOR POSITIONS
def bombe(inpt,output,test):
    inputn = [num[x] for x in inpt]
    outputn = [num[x] for x in output]
    t = num[test]
    stops = []
    for x in range(26):
        for y in range(26):
            for z in range(26):
                lis = poslist([x,y,z],len(inputn))
                for guess in [[t,x] for x in range(26)]:
                    if contradiction2(inputn,outputn,lis,guess):
                        stops.append(let[x]+let[y]+let[z] + ' ' + let[guess[0]]+let[guess[1]])
    return(stops)

# SEARCH BY RING SETTINGS
def authenticbombe(inpt,output,test):
    global rings
    inputn = [num[x] for x in inpt]
    outputn = [num[x] for x in output]
    t = num[test]
    stops = []
    lis = poslist([num[x] for x in ['y','y','e']],len(inputn))
    for x in range(26):
        for y in range(26):
            for z in range(26):
                enigma.rings = [x,y,z]
                for guess in [[t,x] for x in range(26)]:
                    if contradiction2(inputn,outputn,lis,guess):
                        stops.append(let[x]+let[y]+let[z] + ' ' + let[guess[0]]+let[guess[1]])
    return(stops)

rot = [rII,rI,rIII]
rin = ['j','g','n']
notch = ['e','q','v']
ref = rB
test = 't'
plg = []
init(rot,rin,notch,ref,plg)

inpt = 'qatctqcnwmtvc'
output = 'secretmessage'

t = time.clock()
stops = bombe(inpt,output,test)
print('position stops: ',stops,len(stops),time.clock() - t)
t = time.clock()
stops = authenticbombe(inpt,output,test)
print('ring stops: ',stops,len(stops),time.clock() - t)