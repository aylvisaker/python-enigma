import random
import time

def shift(l,n):
    return(l[n:] + l[:n])

alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
code = {}
for i, l in enumerate(alphabet):
    code[i] = l
    code[l] = i
    code[str(i)] = i

def encodestring(text):
    out = []
    for letter in text:
        out.append(code[letter])
    return(tuple(out))
def decodetuple(numbertuple):
    return(''.join([code[x] for x in numbertuple]))

rotorlist = [
    'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
    'AJDKSIRUXBLHWTMCQGZNPYFVOE',
    'BDFHJLCPRTXVZNYEIWGAKMUSQO',
    'ESOVPZJAYQUIRHXLNFTGKDCMWB',
    'VZBRGITYUPSDNHLXAWMJQOFECK',
    'JPGVOUMFYQBENHZRDKASXLICTW',
    'NZJHGRCXMYSWBOUFAIVLPEKQDT',
    'FKQHTLXOCBJSPDZRAMEWNIUYGV',
    'LEYJVCNIXWPBQMDRTAKZGFUHOS',
    'FSOKANUERHMBTIYCWLQPZXVGJD',
    'EJMZALYXVBWFCRQUONTSPIKHGD',
    'YRUHQSLDPXNGOKMIEBFZCWVJAT',
    'FVPJIAOYEDRZXWGCTKUQSBNMHL',
    'ENKQAUYWJICOPBLMDXZVFTHRGS',
    'RDOBJNTKVEHMLFCWZAXGYIPSUQ',
    alphabet]
rotornames = ['I','II','III','IV','V','VI','VII','VIII',
    'Beta','Gamma','A','B','C','BT','CT','ETW']
if len(rotorlist)!=len(rotornames): print("ERROR")
notchlist = ['Q','E','V','J','Z','ZM','ZM','ZM']

# Dictionaries for later reference
rotorinitial = {}
for i, r in enumerate(rotornames):
    rotorinitial[r] = [code[x] for x in rotorlist[i]]
notchinitial = {'ETW':[0]}
for i, r in enumerate(rotornames[0:len(notchlist)]):
    notchinitial[r] = [code[x] for x in notchlist[i]]

# Invert a rotor
def inverse(numberlist):
    out = list(range(26))
    for index, inpt in enumerate(numberlist):
        out[inpt] = index
    return(out)

class enigma:
    def __init__(self, umkehrwalze, walzen, ringstellung, steckerbrett):
        # Define names for readable lists of rotors, ring settings, and plugboard pairs
        self.Wplain = walzen.split(' ')
        if len(self.Wplain) == 3: self.Wplain.append('ETW')
        self.Uplain = umkehrwalze
        self.Rplain = [code[x] for x in list(ringstellung)]
        self.Splain = steckerbrett.split(' ')
        # Define nextset: dictionary, returns next setting (rightmost 3 only)
        self.nextset = {}
        notches = [notchinitial[self.Wplain[x]] for x in range(4)]
        for i in range(26):
            for j in range(26):
                for k in range(26):
                    thispos = (i,j,k)
                    # Account for the double-step
                    a, b, c = i, j, (k + 1) % 26
                    if j in notches[-2]:
                        a = (a + 1) % 26
                        b = (b + 1) % 26
                    elif k in notches[-1]:
                        b = (b + 1) % 26
                    self.nextset[thispos] = (a,b,c)
        # Define rot / inv: list, contains N lists of 26 lists (mappings)
        # Define ref: list containing 26 single mappings
        self.rot = [[],[],[],[]]
        self.inv = [[],[],[],[]]
        self.ref = rotorinitial[self.Uplain]
        self.exp = {}
        for i in range(4): #i is the rotor
            v = self.Rplain[i] #look up ring setting
            for j in range(0,26): #j is the position showing
                v = j - v #actual offset vector = position - ring
                z = [] #this will be the mapping for rotor i in setting j
                for k in range(26): #k is the input
                    inpt = (k + v) % 26
                    z.append((rotorinitial[self.Wplain[i]][inpt] - v) % 26)
                (self.rot[i]).append(z)
                (self.inv[i]).append(inverse(z))
    def encipher(self, settings, message):
        s, out = settings, []
        for p in message:
            s = self.nextset[s]
            c = p
            [i,j,k] = s
            c = self.exp[2,k,c]
            c = self.exp[1,j,c]
            c = self.exp[0,i,c]
            c = self.ref[c]
            c = self.exp[0,i,c]
            c = self.exp[1,j,c]
            c = self.exp[2,k,c]            
            ##c = self.rot[2][k][c]
            ##c = self.rot[1][j][c]
            ##c = self.rot[0][i][c]
            ##c = self.ref[c]
            ##c = self.inv[0][i][c]
            ##c = self.inv[1][j][c]
            ##c = self.inv[2][k][c]
            #for i in reversed(range(4)):
            #    c = self.rot[i][s[i]][c]
            #c = self.ref[c]
            #for i in range(4):
            #    c = self.inv[i][s[i]][c]
            out.append(c)
        return(tuple(out))

t = time.clock()
settings = 'AAA'
scode = encodestring(settings)
plaintext = 'AAAAAAAAAA'
n = 250
plaintext = ''.join(['A' for x in range(n)])
pcode = encodestring(plaintext)
machine = enigma('B','I II III','BBB','')
ccode = machine.encipher(scode, pcode)
ciphertext = decodetuple(ccode)
dcode = machine.encipher(scode, ccode)
print(pcode==dcode)
t = time.clock() - t
print('%.2f' % (t*1000))
print(int(2*n/t))
        



# print(shift(alphabet,-3))
# xyz
# print(alphabet)
# abc
# print(shift(alphabet,3))
# def
