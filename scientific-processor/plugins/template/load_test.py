from ctypes import *

cdll.LoadLibrary("build/template.so")
libc = CDLL("build/template.so")

string1 = "/home/buele/git/ichnosat/scientific-processor/inbox/"
string2 = "/home/buele/git/ichnosat/scientific-processor/outbox/"
productPath = string1.encode('utf-8')
destinationPath = string2.encode('utf-8')
libc.process.argtypes = [c_char_p]

print(libc.process(productPath,destinationPath))
