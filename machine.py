import random
import time
import sys
import itertools

# MISCELLANEOUS SIMPLE TOOLS
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
let = {i:alphabet[i] for i in xrange(26)}
num = {alphabet[i]:i for i in xrange(26)}
for x, y in zip(alphabet, range(26)):
    let[x] = x
    num[y] = y

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
    """
    def __init__(self, rotors = ['I', 'II', 'III'], rings = 'AAA', reflector = 'B', plugboard = '', position = 'AAA'):
        """
        Initialize an instance of of the enigma class.
        :param rotors: list of rotor names (I - VIII)
        :param rings: string containing the ring settings (Ringstellung)
        :param reflector: reflector name (A, B, C, Bt, or Ct)
        :param plugboard: string with pairs of adjacent characters representing plugboard connections
        :param position: string representing position of the rotors
        """
        # rotors is a list of dictionaries representing the machine's rotors.
        self.rotors = [{x: num[rotorCollection[rot][x]] for x in range(26)} for rot in rotors]
        # rotorInverses is a list of dictionaries representing the reverse pathway through the rotors.
        self.rotorInverses = [{y: x for x, y in rot.items()} for rot in self.rotors]
        # ringsettings is a list containing numerical values for the machine's ring settings.
        self.ringsettings = [num[x] for x in rings]
        # notches is a list containing locations where the rotor triggers its left neighbor to rotate.
        self.notches = [[num[x] for x in notches[rot]] for rot in rotors]
        # reflector is a dictionary representing the machine's reflector.
        self.reflector = {x: num[reflectorCollection[reflector][x]] for x in range(26)}
        # plugboard is a dictinoary representing the machine's plugboard.
        self.plugBoard = {x: x for x in range(26)}
        for x in range(0, len(plugboard), 2):
            self.plugBoard[num[plugboard[x]]] = num[plugboard[x + 1]]
            self.plugBoard[num[plugboard[x + 1]]] = num[plugboard[x]]
        # positions is a list containing the current position of the rotors
        self.positions = [num[x] for x in position]
        # update all dictionaries so they can work modulo 26
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
        # If input is not a letter, don't do anything.
        if not x in range(26):
            return(x)
        # Step the rotors by one position.
        self.stepRotors()
        # Compute the offsets from positions and ring settings.
        offsets = [self.positions[i] - self.ringsettings[i] for i in range(len(self.positions))]
        # First pass through the plugboard.
        y = self.plugBoard[x]
        # Pass through the rotors from right to left.
        for off, rot in zip(offsets[::-1], self.rotors[::-1]):
            y = (rot[y + off] - off)
        # Pass through the reflector
        y = self.reflector[y]
        # Pass through the rotors from left to right.
        for off, rot in zip(offsets, self.rotorInverses):
            y = (rot[y + off] - off)
        # Second pass through the plugboard.
        y = self.plugBoard[y]
        return y

    def stepRotors(self):
        """
        Steps the rotors by one position.
        """
        output = self.positions
        # Check if the middle rotor has reached one of its notches.
        if self.positions[1] in self.notches[1]:
            output[0] = (output[0] + 1) % 26
            output[1] = (output[1] + 1) % 26
        # Check if the rightmost rotor has reached one of its notches.
        if self.positions[2] in self.notches[2]:
            output[1] = (output[1] + 1) % 26
        # Step the rightmost rotor.
        output[2] = (output[2] + 1) % 26
        self.positions = output

    def encryptMessage(self, message):
        """
        Encrypts or decrypts a message on the Enigma machine.
        :param message: Input (typed on the keyboard)
        :return: Output (read off the lightboard)
        """
        # Convert the message to a list of integers if not done already.
        if not message[0] in range(26):
            output = convert(message)
        else:
            output = message
        # Encrypt / decrypt the message.
        return [self.encryptCharacter(x) for x in output]

class bombe(object):
    """
    A class representing an instance of the Bombe machine with crib wired in.
    """
    def __init__(self, cipher, plain, n = 3):
        """
        Initialize an instance of the bombe class.
        :param cipher: cipher text
        :param plain: plain text
        """
        # Convert cipher / plain text to numeric data if not done already.
        if cipher[0] in range(26):
            self.cipher = cipher
        else:
            self.cipher = convert(cipher)
        if plain[0] in range(26):
            self.plain = plain
        else:
            self.plain = convert(plain)
        self.numberrotors = n

    def findsolution(self):
        """
        Search through all rotor / reflector configurations.
        :return:
        """
        for ref in reflectorCollection.iterkeys():
            for rots in itertools.combinations(rotorCollection.iterkeys(), 3):
                emachine = enigma(rots, 'AAA', ref, '', 'AAA')
                self.findcontradiction(emachine)

    def findcontradiction(self, emachine):
        """
        Search for a contradiction in the crib.
        """
        positions = itertools.combinations_with_replacement(alphabet, 3)
        plugguess = {x: x for x in range(26)}
        for pos in positions:
            emachine.setPosition(pos)

            emachine.encryptMessage(self.cipher)

        return "i dunno, probably"

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
    ciphertext = convert(ciphertext)
    t = time.clock() - t
    print 'Converting messages to numerical lists (and back) at ' + str(int(2 * n / t)) + ' characters per second'
    n = 5000
    t = time.clock()
    for x in range(n):
        machine = enigma(rotors, rings, reflector, plugboard, position)
    t = time.clock() - t
    print 'Initializing machines ' + str(int(n / t)) + ' times per second.'

def main():
    if len(sys.argv) <= 1:
        test()
    else:
        print "I don't understand arguments yet."

if __name__ == "__main__":
    main()
