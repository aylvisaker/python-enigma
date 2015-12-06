import random
import time
#import collections

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
rotor['I-r']    = 'JGDQOXUSCAMIFRVTPNEWKBLZYH'
rotor['II-r']   = 'NTZPSFBOKMWRCJDIVLAEYUXHGQ'
rotor['III-r']  = 'JVIUBHTCDYAKEQZPOSGXNRMWFL'
rotor['UKW-r']  = 'QYHOGNECVPUZTFDJAXWMKISRBL'
rotor['ETW-r']  = 'QWERTZUIOASDFGHJKPYXCVBNML'
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
rotor['Dum']    = alphabet
notch = {}
notch['I']      = ['Q']
notch['II']     = ['E']
notch['III']    = ['V']
notch['IV']     = ['J']
notch['V']      = ['Z']
notch['VI']     = ['Z','M']
notch['VII']    = ['Z','M']
notch['VIII']   = ['Z','M']

rgs = 'ZZDG'
rts = ['Beta','VI','I','III']
rfs = 'B-Thin'

rot = {}
inv = {}
ref = {}
dum = {}
#for i in range(26):
#	rot[0,'A',conv[i]] = rotor['Beta'][i]
#	rot[1,'A',conv[i]] = rotor['VI'][i]
#	rot[2,'A',conv[i]] = rotor['I'][i]
#	rot[3,'A',conv[i]] = rotor['III'][i]
#	inv[0,'A',rotor['Beta'][i]] = conv[i]
#	inv[1,'A',rotor['VI'][i]] = conv[i]
#	inv[2,'A',rotor['I'][i]] = conv[i]
#	inv[3,'A',rotor['III'][i]] = conv[i]
#	ref[conv[i]] = rotor['B-Thin'][i]
#t = time.clock()
for i in alphabet:
	ref[i] = rotor[rfs][conv[i]]
	for p in alphabet:
		for r in range(4):
			ii = conv[i]
			pp = conv[p] - conv[rgs[r]]
			rr = [conv[x] for x in rotor[rts[r]]]
			#rot[r,p,i] = conv[(conv[rot[r,'A',conv[(conv[i] + conv[p])%26]]] - conv[p]) % 26]
			#inv[r,p,i] = conv[(conv[inv[r,'A',conv[(conv[i] + conv[p])%26]]] - conv[p]) % 26]
			rot[r,p,i] = conv[(rr[(ii + pp) % 26] - pp) % 26]
			inv[r,p,rot[r,p,i]] = i
#print(time.clock() - t)
plugs = 'BQ CR DI EJ KW MT OS PX UZ GH'
pb = {}
for letter in alphabet:
        pb[letter] = letter
for pair in plugs.split(' '):
        pb[pair[0]] = pair[1]
        pb[pair[1]] = pair[0]

def enigmaC(positions,plain):
	pos = list(positions)
	cha = list(plain)
	for n in range(len(cha)):
		if pos[3] in notch[rts[3]]:
			pos[2] = shift[pos[2]]
		elif pos[2] in notch[rts[2]]:
			pos[2] = shift[pos[2]]
			pos[1] = shift[pos[1]]
		pos[3] = shift[pos[3]]
		x = cha[n]
		x = pb[x]
		x = rot[3,pos[3],x]
		x = rot[2,pos[2],x]
		x = rot[1,pos[1],x]
		x = rot[0,pos[0],x]
		x = ref[x]
		x = inv[0,pos[0],x]
		x = inv[1,pos[1],x]
		x = inv[2,pos[2],x]
		x = inv[3,pos[3],x]
		x = pb[x]
		cha[n] = x
	return(''.join(cha))

n = 10000
longplain = ''.join([conv[random.randint(0,25)] for x in range(n)])
t = time.clock()
longcipher = enigmaC('AXMZ',longplain)
longdecipher = enigmaC('AXMZ',longcipher)
print(str(int(2*n / (time.clock() - t))) + ' characters per second')
if longplain==longdecipher:
	print('all is well')
else: print('there was an error')

cipher = 'HCEYZTCSOPUPPZDICQRDLWXXFACTTJMBRDVCJJMMZRPYIKHZAWGLYXWTMJPQUEFSZBOTVRLALZXWVXTSLFFFAUDQFBWRRYAPSBOWJMKLDUYUPFUQDOWVHAHCDWAUARSWTKOFVOYFPUFHVZFDGGPOOVGRMBPXXZCANKMONFHXPCKHJZBUMXJWXKAUODXZUCVCXPFT'
plain = 'BOOTKLARXBEIJSCHNOORBETWAZWOSIBENXNOVXSECHSNULCBMXPROVIANTBISZWONULXDEZXBENOETIGEGLMESERYNOCHVIEFKLHRXSTEHEMARQUBRUNOBRUNFZWOFUHFXLAGWWIEJKCHAEFERJXNNTWWWFUNFYEINSFUNFMBSTEIGENDYGUTESIWXDVVVJRASCH'
print(enigmaC('NAQL',cipher))

#a = [1,2,3,4,5]
#a.append(a.pop(0))

#import collections
#a = collections.deque([1,2,3,4,5])
#a.rotate(-1)
