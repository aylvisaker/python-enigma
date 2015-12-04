from enigma.machine import EnigmaMachine
import time

machine = EnigmaMachine.from_key_sheet(
	rotors = 'I II III',
	reflector = 'B',
	ring_settings = [0,0,0],
	plugboard_settings = '')

machine.set_display('AAA')
cipher = machine.process_text('HELLOWORLD')
print(cipher)

t = time.clock()
n=10000
longplain = ''.join(['A' for x in range(n)])
t = time.clock()
cipher = machine.process_text(longplain)
decipher = machine.process_text(cipher)
print(2*n/(time.clock()-t))
