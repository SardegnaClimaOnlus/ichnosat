from ctypes import *

cdll.LoadLibrary("build/template.so")
libc = CDLL("build/template.so")

source = "/home/buele/git/ichnosat/scientific-processor/inbox/S2A_OPER_PRD_MSIL1C_PDMC_20161018T110501_R022_V20161016T101022_20161016T101019/"
destination = "/home/buele/git/ichnosat/scientific-processor/outbox/S2A_OPER_PRD_MSIL1C_PDMC_20161018T110501_R022_V20161016T101022_20161016T101019/"
productPath = source.encode('utf-8')
destinationPath = destination.encode('utf-8')
libc.process.argtypes = [c_char_p]

libc.process(productPath,destinationPath)
