from ctypes import *

cdll.LoadLibrary("build/template.so")
libc = CDLL("build/template.so")
print(libc.sum(3, 3))