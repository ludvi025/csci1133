from subprocess import Popen, PIPE, STDOUT

p = Popen(["python", "mod.py"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

ls_stdout, ls_stderr = p.communicate(input='\'hi\''.encode('utf-8'))
print(ls_stdout.decode('utf-8'))
