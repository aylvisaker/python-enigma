import random
import time
import sys

# MISCELLANEOUS SIMPLE TOOLS
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
let = {i:alphabet[i] for i in xrange(26)}
num = {alphabet[i]:i for i in xrange(26)}

# HISTORICALLY ACCURATE ENIGMA ROTORS
rotorCollection = {'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
                   'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
                   'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
                   'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
                   'V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
                   'VI': 'JPGVOUMFYQBENHZRDKASXLICTW',
                   'VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
                   'VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV'}

# THE NOTCH(ES) TRIGGERING TURNOVER IN THE NEXT ROTOR
notches = {'I': 'Q',
           'II': 'E',
           'III': 'V',
           'IV':'J',
           'V': 'Z',
           'VI': 'ZM',
           'VII': 'ZM',
           'VIII': 'ZM'}

# REFLECTORS
reflectorCollection = {'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
                       'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
                       'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
                       'Bt': 'ENKQAUYWJICOPBLMDXZVFTHRGS',
                       'Ct': 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'}

def convert(message):
    if message[0] in range(26):
        return ''.join([let[x] for x in message])
    else:
        return [num[x] for x in message]

class enigma(object):
    """
    A class representing an enigma machine with rotors, reflector, and plugboard configured.
    Rotor positions initially set to 'AAA'.
    """
    def __init__(self, rotors = ['I', 'II', 'III'], rings = 'AAA', reflector = 'B', plugboard = '', position = 'AAA'):
        """
        Initialize an instance of of the machine class.
        :param rotors: list of rotor names (I - VIII)
        :param rings: string containing the ring settings (Ringstellung)
        :param reflector: reflector name (A, B, C, Bt, or Ct)
        :param plugboard: string with pairs of adjacent characters representing plugboard connections
        :param position: string representing position of the rotors
        """
        self.rotors = [{x: num[rotorCollection[rot][x]] for x in range(26)} for rot in rotors]
        self.rotorInverses = [{y: x for x, y in rot.items()} for rot in self.rotors]
        self.ringsettings = [num[x] for x in rings]
        self.notches = [[num[x] for x in notches[rot]] for rot in rotors]
        self.reflector = {x: num[reflectorCollection[reflector][x]] for x in range(26)}
        self.plugBoard = {x: x for x in range(26)}
        for x in range(0, len(plugboard), 2):
            self.plugBoard[num[plugboard[x]]] = num[plugboard[x + 1]]
            self.plugBoard[num[plugboard[x + 1]]] = num[plugboard[x]]
        self.positions = [num[x] for x in position]
        for i in range(26):
            for offset in [-52, -26, 26, 52]:
                for rot in self.rotors:
                    rot[i + offset] = rot[i]
                for rot in self.rotorInverses:
                    rot[i + offset] = rot[i]
                self.plugBoard[i + offset] = self.plugBoard[i]
                self.reflector[i + offset] = self.reflector[i]

    def setPosition(self, position):
        """
        Reset rotor positions
        :param position: desired rotor position
        """
        self.positions = [num[x] for x in position]

    def encryptCharacter(self, x):
        """
        Encrypt a single letter.
        :param x: number in range(26) representing the key pressed
        :return: number in range(26) representing the light activated
        """
        if not x in range(26):
            return(x)
        self.stepRotors()
        offsets = [self.positions[i] - self.ringsettings[i] for i in range(len(self.positions))]
        y = x
        y = self.plugBoard[y]
        for off, rot in zip(offsets[::-1], self.rotors[::-1]):
            y = (rot[y + off] - off)
        y = self.reflector[y]
        for off, rot in zip(offsets, self.rotorInverses):
            y = (rot[y + off] - off)
        y = self.plugBoard[y]
        return y

    def stepRotors(self):
        """
        Steps the rotors by one position.
        """
        output = self.positions
        if self.positions[1] in self.notches[1]:
            output[0] = (output[0] + 1) % 26
            output[1] = (output[1] + 1) % 26
        if self.positions[2] in self.notches[2]:
            output[1] = (output[1] + 1) % 26
        output[2] = (output[2] + 1) % 26
        self.positions = output

    def encryptMessage(self, message):
        """
        Encrypts or decrypts a message on the Enigma machine.
        :param message: Input (typed on the keyboard)
        :return: Output (read off the lightboard)
        """
        if not message[0] in range(26):
            output = convert(message)
        else:
            output = message
        return [self.encryptCharacter(x) for x in output]

def test():
    rotors = ['II', 'VI', 'IV']
    rings = 'ALQ'
    reflector = 'B'
    plugboard = 'AQBOCKDHFUIRJPLYNSWX'
    position = 'RWP'
    ciphertext = 'BNXYWSBGZUCKNYFSUGJZITXDFCDIKTCIVWNOTQLULVEAPRYSOREHNMEKGQORTFTCHQTSCJYCYTBSFBFBAAADZCPGCTYFJUHXDCFV'
    plaintext = 'VONMNAAZWESTFUNKSRUCHEINSACHTVIERSECHSNICHTZUENTSCHLZWSSELNXNACHPRUEFENUNDNEUVERSQHLUESSEPTHERGEBENX'
    machine = enigma(rotors, rings, reflector, plugboard, position)
    decryption = machine.encryptMessage(ciphertext)
    if decryption == convert(plaintext):
        print "Successfully decrypted Enigma ciphertext:"
        print ciphertext
        print "Message reads:"
        print plaintext
        print
    n = 10**5
    plaintext = [random.choice(range(26)) for x in range(n)]
    t = time.clock()
    ciphertext = machine.encryptMessage(plaintext)
    t = time.clock() - t
    print 'Encrypting at ' + str(int(n / t)) + ' characters per second'
    positions = [''.join([random.choice(alphabet) for x in range(3)]) for y in range(n)]
    t = time.clock()
    [machine.setPosition(positions[i]) for i in range(n)]
    t = time.clock() - t
    print 'Switching machine position ' + str(int(n / t)) + ' times per second'
    t = time.clock()
    ciphertext = convert(ciphertext)
    t = time.clock() - t
    print 'Converting messages to numerical lists at ' + str(int(n / t)) + ' characters per second'

def main():
    if len(sys.argv) <= 1:
        test()

if __name__ == "__main__":
    main()