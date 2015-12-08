import enigma
import Tkinter as tk

def onKeyPress(event):
    global plain, cipher, current
    x = event.char
    if x == '0':
        plain = plain[:-1]
    if x == '1':
        plain = ''
    if x == '7': initial[0] = (initial[0] + 1)%26
    if x == '8': initial[1] = (initial[1] + 1)%26
    if x == '9': initial[2] = (initial[2] + 1)%26
    if (x not in enigma.letters): x = ''
    plain = plain + x
    current = [x for x in initial]
    for p in plain:
        current = enigma.rotorstep(current)
    cipher = enigma.enigmaC([enigma.let[x] for x in initial], plain)
    a = current[0] - enigma.rings[0]
    b = current[1] - enigma.rings[1]
    c = current[2] - enigma.rings[2]
    text.delete(1.0,'end')
    text.insert('end',   'initial positions:    ' + ''.join([enigma.let[x] for x in initial]))
    text.insert('end', '\nring settings:        ' + ''.join(rin) + '\n')
    text.insert('end', '\n' + plain)
    text.insert('end', '\n' + cipher + '\n')
    text.insert('end', '\ncurrent position:     ' + ''.join([enigma.let[x] for x in current]))
    text.insert('end', '\nplaintext alphabet:   ' + enigma.letters)
    text.insert('end', '\nplugboard:            ' + ''.join([enigma.let[enigma.pb[x]] for x in range(26)]))
    text.insert('end', '\nright rotor:          ' + ''.join([enigma.let[(enigma.r2[(x + c)%26] - c)%26] for x in range(26)]))
    text.insert('end', '\nmiddle rotor:         ' + ''.join([enigma.let[(enigma.r1[(x + b)%26] - b)%26] for x in range(26)]))
    text.insert('end', '\nleft rotor:           ' + ''.join([enigma.let[(enigma.r0[(x + a)%26] - a)%26] for x in range(26)]))
    text.insert('end', '\nreflector:            ' + ''.join([enigma.let[enigma.r[x]] for x in range(26)]))
    text.insert('end', '\nleft rotor inverse:   ' + ''.join([enigma.let[(enigma.r0i[(x + a)%26] - a)%26] for x in range(26)]))
    text.insert('end', '\nmiddle rotor inverse: ' + ''.join([enigma.let[(enigma.r1i[(x + b)%26] - b)%26] for x in range(26)]))
    text.insert('end', '\nright rotor inverse:  ' + ''.join([enigma.let[(enigma.r2i[(x + c)%26] - c)%26] for x in range(26)]))
    text.insert('end', '\nplugboard:            ' + ''.join([enigma.let[enigma.pb[x]] for x in range(26)]))

rot = [enigma.rII,enigma.rI,enigma.rIII]
rin = ['j','g','n']
notch = ['e','q','v']
ref = enigma.rB
plg = ['nk','er','ay','tj','cb','qm','sl','wo','ig','fh']
enigma.init(rot,rin,notch,ref,plg)

plain = ''
cipher = ''
initial = [enigma.num[x] for x in ['y','y','e']]

root = tk.Tk()
text = tk.Text(root, background='white', foreground='black', font=('Courier New', 24))
text.pack()
root.bind('<KeyPress>', onKeyPress)
root.mainloop()
