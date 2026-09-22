import os
os.fork()
print(os.getpid(), os.getppid())
