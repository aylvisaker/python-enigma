import time

letters = 'abcdefghijklmnopqrstuvwxyz'
let = {i:letters[i] for i in range(26)}
let['+'] = '+'
num = {let[i]:i for i in range(26)}
num['+'] = '+'

rI = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'.lower()
rII = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'.lower()
rIII = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'.lower()
rIV = 'ESOVPZJAYQUIRHXLNFTGKDCMWB'.lower()
rV = 'VZBRGITYUPSDNHLXAWMJQOFECK'.lower()
rVI = 'JPGVOUMFYQBENHZRDKASXLICTW'.lower()
rVII = 'NZJHGRCXMYSWBOUFAIVLPEKQDT'.lower()
rVIII = 'FKQHTLXOCBJSPDZRAMEWNIUYGV'.lower()

notches = [['q'],['e'],['v'],['j'],['z'],['z','m'],['z','m'],['z','m']]

rA = 'EJMZALYXVBWFCRQUONTSPIKHGD'.lower()
rB = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'.lower()
rC = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'.lower()
rBt = 'ENKQAUYWJICOPBLMDXZVFTHRGS'.lower()
rCt = 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'.lower()

# MACHINE SETUP (ROTORS, RING SETTINGS, NOTCHES, REFLECTOR, PLUGBOARD)
def init(rot,rin,notch,ref,plg):
    global r0, r1, r2, r0i, r1i, r2i, r, pb, rings, notches
    r0 = {i:num[rot[0][i]] for i in range(26)}
    r1 = {i:num[rot[1][i]] for i in range(26)}
    r2 = {i:num[rot[2][i]] for i in range(26)}
    r0i = {y:x for x, y in r0.items()}
    r1i = {y:x for x, y in r1.items()}
    r2i = {y:x for x, y in r2.items()}
    r = {i:num[ref[i]] for i in range(26)}
    pb1 = {num[x[0]]:num[x[1]] for x in plg}
    pb2 = {num[x[1]]:num[x[0]] for x in plg}
    leftover = letters
    for x in plg:
        leftover = leftover.replace(x[0],'')
        leftover = leftover.replace(x[1],'')
    pb3 = {num[x]:num[x] for x in leftover}
    pb = dict( list(pb1.items()) + list(pb2.items()) + list(pb3.items()) )
    rings = [num[x] for x in rin]
    notches = [num[x] for x in notch]

# ENCRYPT SINGLE CHARACTER (NUMBERED POSITION, NUMBER)
def single(pos,x):
    if x == '+':
        return('+')
    a = pos[0] - rings[0]
    b = pos[1] - rings[1]
    c = pos[2] - rings[2]
    out = x
    out = pb[out]
    out = (r2[(out + c)%26] - c)%26
    out = (r1[(out + b)%26] - b)%26
    out = (r0[(out + a)%26] - a)%26
    out = r[out]
    out = (r0i[(out + a)%26] - a)%26
    out = (r1i[(out + b)%26] - b)%26
    out = (r2i[(out + c)%26] - c)%26
    out = pb[out]
    return(out)

# STEP THE ROTORS AFTER KEYPRESS / BEFORE ENCRYPTION (NUMBERED POSITION)
def rotorstep(posit):
    out = posit
    if out[1] == notches[1]:
        out[0] = (out[0] + 1)%26
        out[1] = (out[1] + 1)%26
    if out[2] == notches[2]:
        out[1] = (out[1] + 1)%26
    out[2] = (out[2] + 1)%26
    return(out)

# SET UP POSITION LIST OF LENGTH N
def poslist(poss,n):
    init = [x for x in poss]
    out = [init]
    for i in range(1,n+1):
        temp = [x for x in rotorstep(out[i-1])]
        out.append(temp)
    return(out)

# ENCRYPT A MESSAGE (LETTERED POSITION, MESSAGE)
def enigmaC(pos,x):
    out = []
    posn = [num[x] for x in pos]
    for i in x:
        posn = rotorstep(posn)
        out.append(let[single(posn,num[i])])
    return ''.join(out)

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
                rings = [x,y,z]
                for guess in [[t,x] for x in range(26)]:
                    if contradiction2(inputn,outputn,lis,guess):
                        stops.append(let[x]+let[y]+let[z] + ' ' + let[guess[0]]+let[guess[1]])
    return(stops)

# INITIALIZATION EXAMPLE
rot = [rII,rI,rIII]
rin = ['j','g','n']
notch = ['e','q','v']
ref = rB
plg = ['nk','er','ay','tj','cb','qm','sl','wo','ig','fh']
init(rot,rin,notch,ref,plg)

# DECRYPTION EXAMPLE
#pos = ['y','y','e']
#input = 'qatctqcnwmtvcopyvfholcqtvgmtwobrfoubrmqbrihllxdbtzlxlgzuqfcwpxpokolffadxdavtjm'
#print(enigmaC(pos,input))

# BOMBE EXAMPLE
t = time.clock()
inpt = 'qatctqcnwmtvc'
output = 'secretmessage'
#inpt = 'wetterbericht'
#output = enigmaC(['m','o','q'],inpt)
#output = 'atqbggywcrybg'
#inpt = 'helloworldiamabombeandmyjobistodecryptthismessage'
#output = enigmaC(['p','o','q'],inpt)
test = 't'
plg = []
init(rot,rin,notch,ref,plg)
stops = bombe(inpt,output,test)
print('position / contradiction2: ',stops,len(stops),time.clock() - t)
t = time.clock()
stops = authenticbombe(inpt,output,test)
print('rings    / contradiction2: ',stops,len(stops),time.clock() - t)
#stops = authenticbombe(inpt,output,test)
#print('rings / contradiction2: ',stops,len(stops),time.clock() - t)

# MORE BOMBE EXAMPLES
#rot = [rII,rI,rIII]
#rin = ['j','g','h']
#notch = ['e','q','v']
#ref = rB
#plg = ['qw','er','tz','ui','op','ak','yx','cv','bn','ml']
#init(rot,rin,notch,ref,[])
#inpt = 'dogvlabdizf'
#output = 'ggvlabgizfi'
#test = 'g'
#t = time.clock()
#print(bombe(inpt,output,test),time.clock() - t)
#rings = [0,0,0]
#print(bombe(input,output,test),time.clock() - t)
#print(contradiction2([num[x] for x in input],[num[x] for x in output],poslist([num[x] for x in ['y','y','y']],len(input)),[0,24]))

plain = ''
cipher = ''
initial = [num[x] for x in ['y','y','e']]