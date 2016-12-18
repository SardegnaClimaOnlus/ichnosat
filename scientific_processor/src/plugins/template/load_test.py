from ctypes import *

cdll.LoadLibrary("build/template.so")
libc = CDLL("build/template.so")

source = "/usr/ichnosat/scientific_processor/inbox/01/"
destination = "/usr/ichnosat/scientific_processor/outbox/01/"
productPath = source.encode('utf-8')
destinationPath = destination.encode('utf-8')
libc.process.argtypes = [c_char_p]

libc.process(productPath,destinationPath)
