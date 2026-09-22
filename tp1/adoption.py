import os, time

if os.fork() == 0:
    time.sleep(1)
    print(os.getppid())