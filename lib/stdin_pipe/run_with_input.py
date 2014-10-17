from subprocess import Popen, PIPE, STDOUT
import sys

def run(script, user_input):
    p = Popen([sys.executable, script], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    out, err = p.communicate(input=user_input.encode('utf-8'))
    if out:
        out = out.decode('utf-8')
    if err:
        err = err.decode('utf-8')
    return out, err

def runInteractive(script, user_input):
    p = Popen([sys.executable, '-i', script], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    out, err = p.communicate(input=user_input.encode('utf-8'))
    if out:
        out = out.decode('utf-8')
    if err:
        err = err.decode('utf-8')
    return out, err
