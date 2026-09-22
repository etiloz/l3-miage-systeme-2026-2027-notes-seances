import os, sys

def exec_cmd(cmd, background=False):
    args = cmd.strip().split()
    for i, arg in enumerate(args):
        if arg.startswith('$'):
            env_var = arg[1:]
            args[i] = os.environ.get(env_var, '')
    pid = os.fork()
    if pid == 0:
        try:
            os.execvp(args[0], args)
        except FileNotFoundError:
            print(args[0], ": commande non trouvée")
            sys.exit(1)
        except PermissionError:
            print(f"{args[0]}: permission non accordée")
            sys.exit(1)
    else:
        if not background:
            while True:
                pid2, status = os.wait()
                if pid2 == pid:
                    os.environ['?'] = str(os.WEXITSTATUS(status))
                    return status
                else:
                    for i, job in enumerate(jobs):
                        if job[0] == pid2:
                            jobs[i] = (job[0], job[1], "Done")
        else:
            return pid 

history = []
jobs = []

while True:
    try:
        cmd = input("% ")
    except EOFError:
        break
    cmd = cmd.strip()
    if cmd != "":
        history.append(cmd)
    if cmd.endswith('&'):
        cmd = cmd[:-1].strip()
        if cmd != "":
            pid = exec_cmd(cmd, background=True)
            jobs.append((pid, cmd, "Running"))
        continue
    if ";" in cmd:
        cmd1,cmd2 = cmd.split(";")
        exec_cmd(cmd1)
        exec_cmd(cmd2)
        continue
    if "&&" in cmd:
        cmd1,cmd2 = cmd.split("&&")
        status = exec_cmd(cmd1)
        if status == 0:
            exec_cmd(cmd2)
        continue
    args = cmd.split()
    if args[0] == 'exit':
        if len(args) > 1:
            try:
                exit_code = int(args[1])
            except ValueError:
                print("exit: argument numérique requis")
                continue
            sys.exit(exit_code)
        else:
            sys.exit(0)
    elif args[0] == "cd":
        try:
            os.chdir(args[1])
            os.environ['OLDPWD'] = os.environ.get('PWD', '')
            os.environ['PWD'] = os.getcwd()
        except FileNotFoundError:
            print(f"cd: {args[1]}: Aucun fichier ou dossier de ce type")
        except PermissionError:
            print(f"cd: {args[1]}: permission non accordée")
    elif cmd == 'env':
        for key in os.environ:
            print(f"{key}={os.environ[key]}")
    elif cmd == 'history':
        for i, h in enumerate(history):
            print(f"{i+1} {h}")
    elif args[0] == 'export':
        if len(args) == 2 and '=' in args[1]:
            key, value = args[1].split('=', 1)
            os.environ[key] = value
        else:
            print("export: format incorrect, utilisez export VAR=VALUE")
    elif cmd == 'jobs':
        # actualiser l'état des jobs
        for i, job in enumerate(jobs):
            pid, cmd, status = job
            try:
                pid2, stat = os.waitpid(pid, os.WNOHANG)
                if pid2 == pid: # <- il y a un zombie de pid égal à pid
                    jobs[i] = (pid, cmd, "Done")
            except ChildProcessError:
                jobs[i] = (pid, cmd, "Done")
        for i, job in enumerate(jobs):
            print(f"[{i+1}] {job[2]} {job[1]} (PID: {job[0]})")
    elif args[0] == 'fg':
        if len(args) < 2:
            print("fg: argument requis")
            continue
        job_index = int(args[1]) - 1
        pid, cmd, status = jobs[job_index]
        if status == "Running":
            os.waitpid(pid, 0)
            jobs[job_index] = (pid, cmd, "Done")
    elif cmd != "":
        exec_cmd(cmd)
