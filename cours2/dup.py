import os

fd = os.open("toto.txt", os.O_WRONLY)
fd2 = os.dup(fd)
os.write(fd, b"Hello, world!\n")
os.close(fd)
os.write(fd2, b"Hello, world!\n")
os.close(fd2)