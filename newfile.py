import random
import time
# https://docs.python.org/2/library/collections.html#collections.deque
# append and pop from either side in O(1) time
# list objects copy and incur O(n) memory movement costs
# problem : looking at the middle is O(n) or O(k) instead of O(1)
#import collections
#a = [1,2,3,4,5]
#a.append(a.pop(0))
#import collections
#a = collections.deque([1,2,3,4,5])
#a.rotate(-1)

alphabet = 'abcdefghijklmnopqrstuvwxyz'.upper()
conv = {}
for i in range(26):
    conv[i] = alphabet[i]
    conv[alphabet[i]] = i
    conv[alphabet[i].lower()] = i
shift = {}
for p in alphabet:
    shift[p] = conv[(conv[p] + 1) % 26]


# wiring and historical data found at:
# http://www.cryptomuseum.com/crypto/enigma/index.htm
rotor = {}
rotor['I']      = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
rotor['II']     = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
rotor['III']    = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
rotor['IV']     = 'ESOVPZJAYQUIRHXLNFTGKDCMWB'
rotor['V']      = 'VZBRGITYUPSDNHLXAWMJQOFECK'
rotor['VI']     = 'JPGVOUMFYQBENHZRDKASXLICTW'
rotor['VII']    = 'NZJHGRCXMYSWBOUFAIVLPEKQDT'
rotor['VIII']   = 'FKQHTLXOCBJSPDZRAMEWNIUYGV'
rotor['Beta']   = 'LEYJVCNIXWPBQMDRTAKZGFUHOS'
rotor['Gamma']  = 'FSOKANUERHMBTIYCWLQPZXVGJD'
#rotor['A']      = 'EJMZALYXVBWFCRQUONTSPIKHGD'
#rotor['B']      = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
#rotor['C']      = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
rotor['B-Thin'] = 'ENKQAUYWJICOPBLMDXZVFTHRGS'
rotor['C-Thin'] = 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'
#rotor['ETW']    = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
notch = {}
notch['I']      = ['Q']
notch['II']     = ['E']
notch['III']    = ['V']
notch['IV']     = ['J']
notch['V']      = ['Z']
notch['VI']     = ['Z','M']
notch['VII']    = ['Z','M']
notch['VIII']   = ['Z','M']

# needs to be broken into two parts
# part one: main rotors, plugboard, and nextpos
# part two: greek rotor and reflector
# UHR, UKW-D, and ETW go here
# UHR wiring found at http://people.physik.hu-berlin.de/~palloks/js/enigma/index_en.html
# default values for each variable
# should handle 3 rotor machine as well, warning for historical consistency
def initialize(rgs,rts,rfs,plugs,po):
    rts = rts.split(' ')
    rot = {}
    inv = {}
    ref = {}
    pb  = {}
    for i in alphabet:
        pb[i] = i
        ref[i] = rotor[rfs][conv[i]]
        for p in alphabet:
            for r in range(4):
                ii = conv[i]
                pp = conv[p] - conv[rgs[r]]
                rr = [conv[x] for x in rotor[rts[r]]]
                rot[r,p,i] = conv[(rr[(ii + pp) % 26] - pp) % 26]
                inv[r,p,rot[r,p,i]] = i
    if plugs == '': plugs = 'AA'
    for pair in plugs.split(' '):
        pb[pair[0]] = pair[1]
        pb[pair[1]] = pair[0]
    # worth checking out exp = defaultdict(lambda: defaultdict(dict))
    # usage would change to exp[p0][p1][p2][p3][i] = c
    # initialize all positions on all four rotors
    # c.f. http://stackoverflow.com/a/27809959
    exp = {}
    for i in alphabet:
        w = pb[i]
        for p3 in alphabet:
            x = rot[3,p3,w]
            for p2 in alphabet:
                y = rot[2,p2,x]
                for p1 in alphabet:
                    z = rot[1,p1,y]
                    z = rot[0,po[0],z]
                    z = ref[z]
                    z = inv[0,po[0],z]
                    z = inv[1,p1,z]
                    z = inv[2,p2,z]
                    z = inv[3,p3,z]
                    z = pb[z]
                    exp[''.join([po[0] + p1 + p2 + p3]),i] = z
    nextpos = {}
    for i in alphabet:
        for j in alphabet:
            for k in alphabet:
                inpt = po[0] + i + j + k
                pos = list(inpt)
                # in is O(1) for deques and O(n) for dictionaries
                if pos[3] in notch[rts[3]]:
                    pos[2] = shift[pos[2]]
                elif pos[2] in notch[rts[2]]:
                    pos[2] = shift[pos[2]]
                    pos[1] = shift[pos[1]]
                pos[3] = shift[pos[3]]
                outpt = ''.join(pos)
                nextpos[inpt] = outpt
    return([nextpos,exp])

# take nextpos and exp as inputs initialize by default with:
# rgs = 'AAA' # (or '111')
# rts = 'I II III'
# rfs = 'B'
# plugs = 'QW ER TZ UI OA SD FG HJ KP YX CV BN ML'
def enigma(positions,plain):
    global nextpos
    global exp
    pos = positions[:]
    cha = list(plain)
    x = positions[0]
    for n in range(len(cha)):
        # dictionary searching is O(n)
        # accessing a list is O(1) iterating should be as well
        # consider converting to integers
        pos = nextpos[pos]
        cha[n] = exp[pos,cha[n]]
    return(''.join(cha))

# check the machine against the RASCH message
# make this a function. read messages from text file
rgs = 'ZZDG' # historically given as numbers with A = 1 ... Z = 26
rts = 'Beta VI I III'
rfs = 'B-Thin'
plugs = 'BQ CR DI EJ KW MT OS PX UZ GH'
position = 'NAQL'
[nextpos,exp] = initialize(rgs,rts,rfs,plugs,position)
cipher = ('HCEYZTCSOPUPPZDICQRDLWXXFACTTJMBRDVCJJMMZRPYIKHZAWGLYXWTMJPQUEFSZBOTVR'
    'LALZXWVXTSLFFFAUDQFBWRRYAPSBOWJMKLDUYUPFUQDOWVHAHCDWAUARSWTKOFVOYFPUFHVZ'
    'FDGGPOOVGRMBPXXZCANKMONFHXPCKHJZBUMXJWXKAUODXZUCVCXPFT')
plain  = ('BOOTKLARXBEIJSCHNOORBETWAZWOSIBENXNOVXSECHSNULCBMXPROVIANTBISZWONULXDE'
    'ZXBENOETIGEGLMESERYNOCHVIEFKLHRXSTEHEMARQUBRUNOBRUNFZWOFUHFXLAGWWIEJKCHA'
    'EFERJXNNTWWWFUNFYEINSFUNFMBSTEIGENDYGUTESIWXDVVVJRASCH')
decipher = enigma(position,cipher)
if decipher == plain: print('successfully decrypted historical message')

# benchmark tests for initialization and mapping speed
# turn this into a function of n
# move import of time and random here
n = 1000000
rgs = ''.join([conv[random.randint(0,25)] for x in range(4)])
rts = random.choice(['Beta ','Gamma ']) + ' '.join(random.sample(['I','II','III','IV','V','VI','VII'],3))
rfs = random.choice(['B-Thin','C-Thin'])
cables = random.randint(0,13)
plugorder = random.sample(alphabet,26)
p = [''.join(plugorder[i:i+2]) for i in range(0,25,2)]
plugs = ' '.join(random.sample(p,cables))
position = ''.join([conv[random.randint(0,25)] for x in range(4)])
plain = ''.join([conv[random.randint(0,25)] for x in range(n)])
t1 = time.clock()
[nextpos,exp] = initialize(rgs,rts,rfs,plugs,position)
t1 = (time.clock() - t1) * 1000
print('initialization took ' + str('%.2f' % t1) + ' milliseconds.')
t2 = time.clock()
cipher = enigma(position,plain)
decipher = enigma(position,cipher)
t2 = time.clock() - t2
cps = str(int(2*n / t2))
kps = str(int(2*n / t2 / 250))
if plain == decipher:
    print('mapping at ' + cps + ' characters per second = ' + kps + ' keys per second.')
    upper = (250*26**3/float(cps) + t1/1000)*26 * 2*2*(8*7*6 - 5*4*3) / (3600*24)
    print('lower bound on worst-case bombe run ' + str('%.2f' % upper) + ' days (ignoring steckerbrett and ringstellung)')
else: print(' '.join(['there was an error!',rgs,rts,rfs,plugs,position]))

# bombe code goes here see myenigma.py for help
# required arguments should be restricted to a message and plaintext
# check rotor orderings in prescribed order optional argument forces starting point
# include four-gram analysis of previous messages (see command line options for source)
# c.f. http://practicalcryptography.com/cryptanalysis/breaking-machine-ciphers/cryptanalysis-enigma/
# test against http://users.telenet.be/d.rijmenants/en/challenge.htm

# command line options go here
# call historical check and benchmark checks if no arguments
# arguments for ciphertext and plaintext
# import messages from http://www.enigma.hoerenberg.com/
# detect plaintext input and offer to decrypt
# 
# error handling: https://docs.python.org/2/tutorial/errors.html
