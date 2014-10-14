from subprocess import Popen, PIPE, STDOUT

def run(script, user_input):
    p = Popen(['python', script], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    out, err = p.communicate(input=user_input.encode('utf-8'))
    if out:
        out = out.decode('utf-8')
    if err:
        err = err.decode('utf-8')
    return out, err

def runInteractive(script, user_input):
    p = Popen(['python', '-i', script], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    out, err = p.communicate(input=user_input.encode('utf-8'))
    if out:
        out = out.decode('utf-8')
    if err:
        err = err.decode('utf-8')
    return out, err
