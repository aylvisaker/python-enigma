import random
import time

alphabet = 'abcdefghijklmnopqrstuvwxyz'.upper()
conv = {}
for i in range(26):
	conv[i] = alphabet[i]
	conv[alphabet[i]] = i
	conv[alphabet[i].lower()] = i

rotor = {}
rotor['IC']     = 'DMTWSILRUYQNKFEJCAZBPGXOHV'
rotor['IIC']    = 'HQZGPJTMOBLNCIFDYAWVEUSRKX'
rotor['IIIC']   = 'UQNTLSZFMREHDPXKIBVYGJCWOA'
rotor['I']      = 'JGDQOXUSCAMIFRVTPNEWKBLZYH'
rotor['II']     = 'NTZPSFBOKMWRCJDIVLAEYUXHGQ'
rotor['III']    = 'JVIUBHTCDYAKEQZPOSGXNRMWFL'
rotor['UKW']    = 'QYHOGNECVPUZTFDJAXWMKISRBL'
rotor['ETW']    = 'QWERTZUIOASDFGHJKPYXCVBNML'
rotor['I-K']    = 'PEZUOHXSCVFMTBGLRINQJWAYDK'
rotor['II-K']   = 'ZOUESYDKFWPCIQXHMVBLGNJRAT'
rotor['III-K']  = 'EHRVXGAOBQUSIMZFLYNWKTPDJC'
rotor['UKW-K']  = 'IMETCGFRAYSQBZXWLHKDVUPOJN'
rotor['ETW-K']  = 'QWERTZUIOASDFGHJKPYXCVBNML'
rotor['I']      = [conv[x] for x in 'EKMFLGDQVZNTOWYHXUSPAIBRCJ']
rotor['II']     = [conv[x] for x in 'AJDKSIRUXBLHWTMCQGZNPYFVOE']
rotor['III']    = [conv[x] for x in 'BDFHJLCPRTXVZNYEIWGAKMUSQO']
rotor['IV']     = 'ESOVPZJAYQUIRHXLNFTGKDCMWB'
rotor['V']      = 'VZBRGITYUPSDNHLXAWMJQOFECK'
rotor['VI']     = 'JPGVOUMFYQBENHZRDKASXLICTW'
rotor['VII']    = 'NZJHGRCXMYSWBOUFAIVLPEKQDT'
rotor['VIII']   = 'FKQHTLXOCBJSPDZRAMEWNIUYGV'
rotor['Beta']   = 'LEYJVCNIXWPBQMDRTAKZGFUHOS'
rotor['Gamma']  = 'FSOKANUERHMBTIYCWLQPZXVGJD'
rotor['A']      = 'EJMZALYXVBWFCRQUONTSPIKHGD'
rotor['B']      = [conv[x] for x in 'YRUHQSLDPXNGOKMIEBFZCWVJAT']
rotor['C']      = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
rotor['B-Thin'] = 'ENKQAUYWJICOPBLMDXZVFTHRGS'
rotor['C-Thin'] = 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'
notch = {}
notch['I']      = ['Q']
notch['II']     = ['E']
notch['III']    = ['V']
notch['IV']     = ['J']
notch['V']      = ['Z']
notch['VI']     = ['Z','M']
notch['VII']    = ['Z','M']
notch['VIII']   = ['Z','M']

rot = {}
inv = {}
ref = {}
for i in range(26):
	rot[0,0,i] = rotor['I'][i]
	rot[1,0,i] = rotor['II'][i]
	rot[2,0,i] = rotor['III'][i]
	inv[0,0,rotor['I'][i]] = i
	inv[1,0,rotor['II'][i]] = i
	inv[2,0,rotor['III'][i]] = i
	ref[i] = rotor['B'][i]

for i in range(26):
	for p in range(26):
		rot[0,p,i] = (rot[0,0,(i - p)%26] + p) % 26
		rot[1,p,i] = (rot[1,0,(i - p)%26] + p) % 26
		rot[2,p,i] = (rot[2,0,(i - p)%26] + p) % 26
		inv[0,p,i] = (inv[0,0,(i - p)%26] + p) % 26
                inv[1,p,i] = (inv[1,0,(i - p)%26] + p) % 26
                inv[2,p,i] = (inv[2,0,(i - p)%26] + p) % 26

def enigmaC(positions,plain):
	pos = list(positions)
	cha = [conv[x] for x in plain]
	for n in range(len(cha)):
		pos[2] = (pos[2] + 1) % 26
		if pos[2] == 0:
			pos[1] = (pos[1] + 1) % 26
			if pos[1] == 0:
				pos[0] = (pos[0] + 1) % 26
		x = rot[2,pos[2],cha[n]]
		x = rot[1,pos[1],x]
		x = rot[0,pos[0],x]
		x = ref[x]
		x = inv[0,pos[0],x]
		x = inv[1,pos[1],x]
		x = inv[2,pos[2],x]
		cha[n] = conv[x]
	return(''.join(cha))

n = 10000
longplain = ''.join([conv[random.randint(0,25)] for x in range(n)])
t = time.clock()
longcipher = enigmaC((22,2,3),longplain)
longdecipher = enigmaC((22,2,3),longcipher)
print(str(int(2*n / (time.clock() - t))) + ' characters per second')
if longplain==longdecipher:
	print('all is well')
else: print('there was an error')

a = [1,2,3,4,5]
a.append(a.pop(0))
print(a)

import collections
a = collections.deque([1,2,3,4,5])
a.rotate(-1)
print(a)
a.rotate(-2)
print(a)
