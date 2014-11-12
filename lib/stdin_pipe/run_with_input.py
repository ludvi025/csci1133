from subprocess import Popen, PIPE, STDOUT
import signal, sys

def run(script, user_input):
    p = Popen([sys.executable, script], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    out, err = p.communicate(input=user_input.encode('utf-8'))
    if out:
        out = out.decode('utf-8')
    if err:
        err = err.decode('utf-8')
    return out, err

def runInteractive(script, user_input):
    # Store the original handler and set a new one
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, _graceful_handler)

    p = Popen([sys.executable, '-i', script], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    out, err = p.communicate(input=user_input.encode('utf-8'))
    if out:
        out = out.decode('utf-8')
    if err:
        err = err.decode('utf-8')

    # Restore the handler
    signal.signal(signal.SIGINT, original_sigint)

    return out, err

def _graceful_handler(signum, frame):
    print("\n\033[91mLooks like you pushed Ctrl-C.\033[0m")
    print("Feel free to push it again if you actually want to quit the script.\n")