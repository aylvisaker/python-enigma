import random
import time
import collections

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
rotor['A']      = 'EJMZALYXVBWFCRQUONTSPIKHGD'
rotor['B']      = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
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
	rot[0,'A',conv[i]] = rotor['I'][i]
	rot[1,'A',conv[i]] = rotor['II'][i]
	rot[2,'A',conv[i]] = rotor['III'][i]
	inv[0,'A',rotor['I'][i]] = conv[i]
	inv[1,'A',rotor['II'][i]] = conv[i]
	inv[2,'A',rotor['III'][i]] = conv[i]
	ref[conv[i]] = rotor['B'][i]

for i in alphabet:
	for p in alphabet:
		for r in range(3):
			rot[r,p,i] = conv[(conv[rot[r,'A',conv[(conv[i] - conv[p])%26]]] + conv[p]) % 26]
			inv[r,p,i] = conv[(conv[inv[r,'A',conv[(conv[i] - conv[p])%26]]] + conv[p]) % 26]

def enigmaC(positions,plain):
	pos = list(positions)
	cha = list(plain)
	for n in range(len(cha)):
		pos[2] = shift[pos[2]]
		if pos[2] in notch['III']:
			pos[1] = shift[pos[1]]
		if pos[1] in notch['II']:
			pos[0] = shift[pos[0]]
		x = rot[2,pos[2],cha[n]]
		x = rot[1,pos[1],x]
		x = rot[0,pos[0],x]
		x = ref[x]
		x = inv[0,pos[0],x]
		x = inv[1,pos[1],x]
		x = inv[2,pos[2],x]
		cha[n] = x
	return(''.join(cha))

n = 5000
longplain = ''.join([conv[random.randint(0,25)] for x in range(n)])
t = time.clock()
longcipher = enigmaC('XMZ',longplain)
longdecipher = enigmaC('XMZ',longcipher)
print(str(int(2*n / (time.clock() - t))) + ' characters per second')
if longplain==longdecipher:
	print('all is well')
else: print('there was an error')
print(longplain)

a = [1,2,3,4,5]
a.append(a.pop(0))
print(a)

import collections
a = collections.deque([1,2,3,4,5])
a.rotate(-1)
print(a)
a.rotate(-2)
print(a)
print(a[1])
