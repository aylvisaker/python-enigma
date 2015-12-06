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
notch = {}
# notch settings for the following are unknown
#rotor['IC']     = 'DMTWSILRUYQNKFEJCAZBPGXOHV'
#rotor['IIC']    = 'HQZGPJTMOBLNCIFDYAWVEUSRKX'
#rotor['IIIC']   = 'UQNTLSZFMREHDPXKIBVYGJCWOA'
#rotor['I-r']    = 'JGDQOXUSCAMIFRVTPNEWKBLZYH'
#rotor['II-r']   = 'NTZPSFBOKMWRCJDIVLAEYUXHGQ'
#rotor['III-r']  = 'JVIUBHTCDYAKEQZPOSGXNRMWFL'
#rotor['UKW-r']  = 'QYHOGNECVPUZTFDJAXWMKISRBL'
#rotor['ETW-r']  = 'QWERTZUIOASDFGHJKPYXCVBNML'
#rotor['I-K']    = 'PEZUOHXSCVFMTBGLRINQJWAYDK'
#rotor['II-K']   = 'ZOUESYDKFWPCIQXHMVBLGNJRAT'
#rotor['III-K']  = 'EHRVXGAOBQUSIMZFLYNWKTPDJC'
#rotor['UKW-K']  = 'IMETCGFRAYSQBZXWLHKDVUPOJN'
#rotor['ETW-K']  = 'QWERTZUIOASDFGHJKPYXCVBNML'
rotor['I']      = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
rotor['II']     = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
rotor['III']    = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
rotor['IV']     = 'ESOVPZJAYQUIRHXLNFTGKDCMWB'
rotor['V']      = 'VZBRGITYUPSDNHLXAWMJQOFECK'
rotor['VI']     = 'JPGVOUMFYQBENHZRDKASXLICTW'
rotor['VII']    = 'NZJHGRCXMYSWBOUFAIVLPEKQDT'
rotor['VIII']   = 'FKQHTLXOCBJSPDZRAMEWNIUYGV'
# reflectors and greek rotors do not require notch settings
rotor['Beta']   = 'LEYJVCNIXWPBQMDRTAKZGFUHOS'
rotor['Gamma']  = 'FSOKANUERHMBTIYCWLQPZXVGJD'
rotor['A']      = 'EJMZALYXVBWFCRQUONTSPIKHGD'
rotor['B']      = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
rotor['C']      = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
rotor['B-Thin'] = 'ENKQAUYWJICOPBLMDXZVFTHRGS'
rotor['C-Thin'] = 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'
rotor['Dum']    = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
notch['I']      = ['Q']
notch['II']     = ['E']
notch['III']    = ['V']
notch['IV']     = ['J']
notch['V']      = ['Z']
notch['VI']     = ['Z','M']
notch['VII']    = ['Z','M']
notch['VIII']   = ['Z','M']

def initialize(rgs,rts,rfs,plugs):
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
	for pair in plugs.split(' '):
	        pb[pair[0]] = pair[1]
	        pb[pair[1]] = pair[0]
	return([rot,inv,ref,pb])

def positionlist(initial,length,rts):
	out = []
	pos = list(initial)
	for n in range(length):
		if pos[3] in notch[rts[3]]:
                        pos[2] = shift[pos[2]]
                elif pos[2] in notch[rts[2]]:
                        pos[2] = shift[pos[2]]
                        pos[1] = shift[pos[1]]
                pos[3] = shift[pos[3]]
		out.append(''.join(pos))
	return(out)

def enigma(positions,plain):
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
		# fourth rotor can be treated as part of reflector
		# eliminate two unnecessary lookups
		# reduce size of rot dictionary by 25%
		x = rot[0,pos[0],x]
		x = ref[x]
		x = inv[0,pos[0],x]
		x = inv[1,pos[1],x]
		x = inv[2,pos[2],x]
		x = inv[3,pos[3],x]
		x = pb[x]
		cha[n] = x
	return(''.join(cha))

rgs = 'ZZDG'
# historically these were given as numbers (with A = 1)
rts = ['Beta','VI','I','III']
# space separated string should suffice here
rfs = 'B-Thin'
plugs = 'BQ CR DI EJ KW MT OS PX UZ GH'
t = time.clock()
[rot,inv,ref,pb] = initialize(rgs,rts,rfs,plugs)
t = (time.clock() - t) * 1000
print('initialization took ' + str("%.2f" % t) + ' milliseconds')
position = 'NAQL'
cipher = 'HCEYZTCSOPUPPZDICQRDLWXXFACTTJMBRDVCJJMMZRPYIKHZAWGLYXWTMJPQUEFSZBOTVRLALZXWVXTSLFFFAUDQFBWRRYAPSBOWJMKLDUYUPFUQDOWVHAHCDWAUARSWTKOFVOYFPUFHVZFDGGPOOVGRMBPXXZCANKMONFHXPCKHJZBUMXJWXKAUODXZUCVCXPFT'
plain = 'BOOTKLARXBEIJSCHNOORBETWAZWOSIBENXNOVXSECHSNULCBMXPROVIANTBISZWONULXDEZXBENOETIGEGLMESERYNOCHVIEFKLHRXSTEHEMARQUBRUNOBRUNFZWOFUHFXLAGWWIEJKCHAEFERJXNNTWWWFUNFYEINSFUNFMBSTEIGENDYGUTESIWXDVVVJRASCH'
n = 100000
longplain = ''.join([conv[random.randint(0,25)] for x in range(n)])
randpos = ''.join([conv[random.randint(0,25)] for x in range(4)])
t = time.clock()
longcipher = enigma(randpos,longplain)
longdecipher = enigma(randpos,longcipher)
cps = str(int(2*n / (time.clock() - t)))
print('mapping at ' + cps + ' characters per second')
if longplain==longdecipher:
	print('symmetric encryption test: pass')
else: print('there was an error')
decipher = enigma(position,cipher)
if decipher == plain: print('historical accuracy check: pass')
else: print(decipher)
if positionlist('ZADT',5,['Beta','I','II','III']) == ['ZADU', 'ZADV', 'ZAEW', 'ZBFX', 'ZBFY']: print('position list double-step check: pass')
t = time.clock()
positionlist(randpos,2*n,rts)
pps = str(int(2*n / (time.clock() - t)))
print('positions calculated at a rate of ' + pps + ' per second')
w = 1000000000
ncps = str(int(w/(w/float(cps) - w/float(pps))))
print('mapping could be improved to ' + ncps + ' cps by precomputing positions')
print('fusing reflector to fourth rotor would improve to at least ' + str(int(11 * float(ncps) / 9)) + ' cps (' + str(int(11 * float(cps) / 9)) + ' without precomputing positions)')
periodcheck = positionlist(randpos,26*26*25 + 1,rts)
if periodcheck[0] == periodcheck[-1]: print('period of the machine is accurate')
