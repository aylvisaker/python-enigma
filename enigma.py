import time

letters = 'abcdefghijklmnopqrstuvwxyz'
let = {i:letters[i] for i in range(26)}
let['+'] = '+'
num = {let[i]:i for i in range(26)}
num['+'] = '+'
#        abcdefghijklmnopqrstuvwxyz
rI    = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'.lower()
rII   = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'.lower()
rIII  = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'.lower()
rIV   = 'ESOVPZJAYQUIRHXLNFTGKDCMWB'.lower()
rV    = 'VZBRGITYUPSDNHLXAWMJQOFECK'.lower()
rVI   = 'JPGVOUMFYQBENHZRDKASXLICTW'.lower()
rVII  = 'NZJHGRCXMYSWBOUFAIVLPEKQDT'.lower()
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
    for i in range(26):
        r0[i-26] = r0[i+26] = r0[i-52] = r0[i+52] = r0[i]
        r1[i-26] = r1[i+26] = r1[i-52] = r1[i+52] = r1[i]
        r2[i-26] = r2[i+26] = r2[i-52] = r2[i+52] = r2[i]
        r0i[i-26] = r0i[i+26] = r0i[i-52] = r0i[i+52] = r0i[i]
        r1i[i-26] = r1i[i+26] = r1i[i-52] = r1i[i+52] = r1i[i]
        r2i[i-26] = r2i[i+26] = r2i[i-52] = r2i[i+52] = r2i[i]
        pb[i-26] = pb[i+26] = pb[i-52] = pb[i+52] = pb[i]
        r[i-26] = r[i+26] = r[i-52] = r[i+52] = r[i]
        #r0[i-26] = r0[i+26] = r0[i]
        #r1[i-26] = r1[i+26] = r1[i]
        #r2[i+26] = r2[i]
        #r0i[i+26] = r0i[i]
        #r1i[i-26] = r1i[i+26] = r1i[i]
        #r2i[i-26] = r2i[i+26] = r2i[i]
        #pb[i-26] = pb[i]
        #r[i-26] = r[i]

# ENCRYPT SINGLE CHARACTER (NUMBERED POSITION, NUMBER)
def single(pos,x):
    if x == '+':
        return('+')
    a = (pos[0] - rings[0])#%26
    b = (pos[1] - rings[1])#%26
    c = (pos[2] - rings[2])#%26
    print(a,b,c)
    out = x
    out = pb[out]
    print(let[out])
    #out = (r2[(out + c)%26] - c)%26
    #out = (r1[(out + b)%26] - b)%26
    #out = (r0[(out + a)%26] - a)%26
    out = r2[out + c] - c
    print(let[out])
    print(r2)
    out = r1[out + b] - b
    print(let[out])
    out = r0[out + a] - a
    print(let[out])
    out = r[out]
    print(let[out])
    #out = (r0i[(out + a)%26] - a)%26
    #out = (r1i[(out + b)%26] - b)%26
    #out = (r2i[(out + c)%26] - c)%26
    out = r0i[out + a] - a
    print(let[out])
    out = r1i[out + b] - b
    print(let[out])
    out = r2i[out + c] - c
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
    posn = [num[z] for z in pos]
    for i in x:
        posn = rotorstep(posn)
        out.append(let[single(posn,num[i])])
    return ''.join(out)

# EXAMPLE
#rot = [rII,rI,rIII]
#rin = ['j','g','n']
#notch = ['e','q','v']
#ref = rB
#plg = ['nk','er','ay','tj','cb','qm','sl','wo','ig','fh']
#init(rot,rin,notch,ref,plg)
#pos = ['y','y','e']
#inpt = 'qatctqcnwmtvcopyvfholcqtvgmtwobrfoubrmqbrihllxdbtzlxlgzuqfcwpxpokolffadxdavtjm'
#print(enigmaC(pos,inpt))

#from random import randint
#t = time.clock()
#limit = 1000000
#x = ''.join([let[randint(0,25)] for x in range(limit)])
#t = time.clock()
#y = enigmaC(pos,x)
#z = enigmaC(pos,y)
#print(str(2*limit/(time.clock()-t)) + ' characters per second')
#print(x==z)

rot = [rI,rII,rIII]
rin = ['a','a','a']
notch = ['q','e','v']
ref = rB
plg = []
init(rot,rin,notch,ref,plg)
pos = ['a','a','a']
inpt = 'h'
print(enigmaC(pos,inpt))
