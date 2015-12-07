import random
import time
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

rotor = {}
rotor['I']      = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
rotor['II']     = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
rotor['III']    = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
rotor['IV']     = 'ESOVPZJAYQUIRHXLNFTGKDCMWB'
rotor['V']      = 'VZBRGITYUPSDNHLXAWMJQOFECK'
rotor['VI']     = 'JPGVOUMFYQBENHZRDKASXLICTW'
rotor['VII']    = 'NZJHGRCXMYSWBOUFAIVLPEKQDT'
rotor['VIII']   = 'FKQHTLXOCBJSPDZRAMEWNIUYGV'
# reflectors and greek rotors (do not require notch settings)
rotor['Beta']   = 'LEYJVCNIXWPBQMDRTAKZGFUHOS'
rotor['Gamma']  = 'FSOKANUERHMBTIYCWLQPZXVGJD'
rotor['A']      = 'EJMZALYXVBWFCRQUONTSPIKHGD'
rotor['B']      = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
rotor['C']      = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
rotor['B-Thin'] = 'ENKQAUYWJICOPBLMDXZVFTHRGS'
rotor['C-Thin'] = 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'
rotor['ETW']    = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
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
# UHR and rewireable reflector go here
def initialize(rgs,rots,rfs,plugs,po):
	rts = rots.split(' ')
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
				if pos[3] in notch[rts[3]]:
		                        pos[2] = shift[pos[2]]
                		elif pos[2] in notch[rts[2]]:
                        		pos[2] = shift[pos[2]]
                        		pos[1] = shift[pos[1]]
                		pos[3] = shift[pos[3]]
				outpt = ''.join(pos)
				nextpos[inpt] = outpt
	return([nextpos,exp])

def enigma(positions,plain):
	pos = positions[:]
	cha = list(plain)
	x = positions[0]
	for n in range(len(cha)):
		pos = nextpos[pos]
		cha[n] = exp[pos,cha[n]]
	return(''.join(cha))

# check the machine against the RASCH message
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
print('initialization took ' + str('%.2f' % t1) + ' milliseconds')
t2 = time.clock()
cipher = enigma(position,plain)
decipher = enigma(position,cipher)
t2 = time.clock() - t2
cps = str(int(2*n / t2))
if plain == decipher:
	print('mapping at ' + cps + ' characters per second')
	upper = (250*26*26*26/float(cps) + t1/1000)*26
	print('upper bound on bombe run ' + str('%.2f' % upper) + ' seconds')
else: print(' '.join(['there was an error!',rgs,rts,rfs,plugs,position]))

