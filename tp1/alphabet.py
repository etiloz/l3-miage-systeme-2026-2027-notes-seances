import os , sys, random

alphabet = "abcdefghijklmnopqrstuvwxyz"
first = True
for _ in range(26):
    if os.fork() == 0:
        if first:
            i = random.randint(0, 25)
        print(alphabet[i % 26],end="")
        sys.exit(i)
    else:
        first = False
        pid, status = os.wait()
        i = os.WEXITSTATUS(status)
        i += 1