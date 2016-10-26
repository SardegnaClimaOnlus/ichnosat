from ctypes import *

cdll.LoadLibrary("build/template.so")
libc = CDLL("build/template.so")

##
string1 = "my string 1"
#string2 = "my string 2"

# create byte objects from the strings
cazzo = string1.encode('utf-8')
##b_string2 = string2.encode('utf-8')

# send strings to c function

libc.process.argtypes = [c_char_p]

##

##libc.process.argtypes = [c_wchar_p]
##cazzo = "Hello, World"
print(libc.process(cazzo))
