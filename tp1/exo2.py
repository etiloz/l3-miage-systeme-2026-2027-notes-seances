import os, sys
alphabet = "abcdefghijklmnopqrstuvwxyz"
for c in alphabet:
    if os.fork() == 0 :
        print(c, end="", flush=True)
        sys.exit(0)

for c in alphabet:
    os.wait()

print(".")