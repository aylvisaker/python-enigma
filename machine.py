alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
let = {i:alphabet[i] for i in xrange(26)}
num = {alphabet[i]:i for i in xrange(26)}
rotorCollection = ['EKMFLGDQVZNTOWYHXUSPAIBRCJ',
                   'AJDKSIRUXBLHWTMCQGZNPYFVOE',
                   'BDFHJLCPRTXVZNYEIWGAKMUSQO',
                   'ESOVPZJAYQUIRHXLNFTGKDCMWB',
                   'VZBRGITYUPSDNHLXAWMJQOFECK',
                   'JPGVOUMFYQBENHZRDKASXLICTW',
                   'NZJHGRCXMYSWBOUFAIVLPEKQDT',
                   'FKQHTLXOCBJSPDZRAMEWNIUYGV']
rotorCollection = [[num[y] for y in x] for x in rotorCollection]

class machine(object):
    """
    A class representing an enigma machine with rotors and reflectors configured.
    Set the rotor positions and ready to encrypt.
    """
    def __init__(self, rotors):
        print(1+1)