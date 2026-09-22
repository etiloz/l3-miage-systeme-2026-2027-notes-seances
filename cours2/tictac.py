import os, time, signal

def handle_sigint(signum, frame):
    print("boum!")

# attache le gestionnaire de signal pour SIGINT
signal.signal(signal.SIGINT, handle_sigint)

# SIGINT: le signal rattrapé
# handle_sigint: le gestionnaire de signal exécuté lorsqu'on reçoit SIGINT

pid_fils = os.fork()
if pid_fils == 0:
    while True:
        print("tic")
        time.sleep(1)

else:
    while True:
        time.sleep(1)
        os.kill(pid_fils, signal.SIGINT)  # envoi de signal au fils
        # pid_fils: le destinataire du signal
        # signal.SIGINT: le signal envoyé